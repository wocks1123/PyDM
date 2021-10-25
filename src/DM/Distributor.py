import asyncio
from contextlib import suppress
import os

import zmq, zmq.asyncio

from DM.utils.util import load_config
from DM.BufferQueue import BufferQueue
from DM.Scheduler import Scheduler


class ZDistributor:

    def __init__(self):
        load_config()

        self.id = 0
        self.tasks = BufferQueue()
        self.scheduler = Scheduler()

        self.ctx = zmq.asyncio.Context()

        self.sub_port = int(os.environ.get("RESOURCE_PORT")) # worker -> dist
        self.pub_port = int(os.environ.get("TASK_PORT")) # dist -> worker
        self.m_port = int(os.environ.get("MONITOR_PORT"))  # 모니터에게 리소스를 보내는

        # 워커 초기화 및 태스크 수신
        self.rep_port = int(os.environ.get("DISTRIBUTOR_REP_PORT"))

        self.sub_sock = self.ctx.socket(zmq.SUB)
        self.sub_sock.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub_sock.bind(f"tcp://*:{self.sub_port}")

        self.pub_sock = self.ctx.socket(zmq.PUB)
        self.pub_sock.bind(f"tcp://*:{self.pub_port}")

        self.monitor_sock = self.ctx.socket(zmq.PUB)
        self.monitor_sock.bind(f"tcp://*:{self.m_port}")

        self.rep_sock = self.ctx.socket(zmq.REP)
        self.rep_sock.bind(f"tcp://*:{self.rep_port}")

        self.workers = []


    def post_accept(self, client):
        pass

    def post_close(self, client):
        pass

    def pre_task(self, task_id, task):
        return task_id, task

    def pre_task_send(self, worker, task_id, task_info):
        pass

    def pre_task_start(self, task_id, task):
        pass

    def pre_task_end(self, task_id, task, result):
        pass

    async def sub_resource(self):
        with suppress(asyncio.CancelledError):
            while True:
                data = await self.sub_sock.recv_json()

                worker_name = data.get("body").get("worker_name")
                if worker_name not in self.workers:
                    self.workers.append(worker_name)

                await self.monitor_sock.send_json(data)

                if not data:
                    break

    async def check(self):
        pass

    async def add_worker(self):
        while True:
            packet = await self.rep_sock.recv_json()

            packet_type = packet.get("type")
            packet_data = packet.get("body")

            if packet_type == "TASK":
                self.id += 1
                id, data = self.pre_task(self.id, packet)
                await self.tasks.put((id, data))

                self.rep_sock.send_json({"data": "ok"})
                self.monitor_sock.send_json(packet)

            elif packet_type == "TASK_START":
                self.pre_task_start(packet.get("id"), packet)
                self.rep_sock.send_json({"data": "ok"})
                self.monitor_sock.send_json(packet)
            elif packet_type == "TASK_END":

                self.pre_task_end(
                    packet.get("id"),
                    packet_data.get("task"),
                    packet_data.get("result")
                )
                worker_name = packet_data["worker_name"]
                self.rep_sock.send_json({"data": "ok"})
                self.monitor_sock.send_json(packet)
                await self.scheduler.task_done(worker_name)

            elif packet_type == "INSERT":
                worker_name = packet_data.get("worker_name")
                self.rep_sock.send_json({"data": "ok"})
                await self.scheduler.append(worker_name)
                self.monitor_sock.send_json(packet)
                self.workers.append(worker_name)

            elif packet_type == "DELETE":
                worker_name = packet_data.get("worker_name")
                self.rep_sock.send_json({"data": "ok"})
                await self.scheduler.remove(worker_name)
                self.monitor_sock.send_json(packet)
                self.workers.remove(worker_name)

            elif packet_type == "UPDATE":
                self.monitor_sock.send_json(packet)

            elif packet_type == "MONITOR":
                self.rep_sock.send_json({"data": self.workers})

    async def pub_task(self):
        cnt = 0
        while True:
            data = {
                "task": "task",
                "body": cnt
            }
            cnt += 1
            await self.pub_sock.send_json(data)
            # print("pub_task data", data)
            await asyncio.sleep(1)

    async def process_task(self):
        while True:
            async for task_id, task_info in self.tasks:
                worker = await self.scheduler.get_next()

                self.pre_task_send(worker, task_id, task_info)

                self.pub_sock.send_json({
                    "type": "TASK",
                    "body": {
                        "id": task_id,
                        "worker_name": worker,
                        "task": task_info.get("body"),
                    }
                })

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            tasks = [
                # loop.create_task(self.pub_task()),
                loop.create_task(self.add_worker()),
                loop.create_task(self.sub_resource()),
                loop.create_task(self.process_task()),
            ]
            group = asyncio.gather(*tasks)
            loop.run_until_complete(group)

            pending = asyncio.all_tasks(loop=loop)
            for task in pending:
                task.cancel()
            group = asyncio.gather(*pending, return_exceptions=True)
            loop.run_until_complete(group)
            loop.close()
        except KeyboardInterrupt:
            print("\nexit...")
