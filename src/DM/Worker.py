import asyncio
from contextlib import suppress
import os

import zmq, zmq.asyncio


from DM.utils.util import load_config, get_cpuinfo, get_cpucore, get_gpuname, get_memoryinfo, get_gpuinfo



###############################################################################
# Monitor에 전송할 데이터를 생성하는 함수

def get_insertdata(worker_name):
    cpu_core = get_cpucore()
    gpu_names = get_gpuname()
    memory_info = get_memoryinfo()["memory_total"] / 1024 / 1024 / 1024
    memory_info = round(memory_info, 2)
    _, gpu_memory, _ = get_gpuinfo()
    gpu_info = list(map(lambda x: round(x["gpu_total"] / 1024, 2), gpu_memory))
    gpu_info = list(map(lambda x: {"name": x[0], "memory": x[1]}, list(zip(gpu_names, gpu_info))))

    return dict(
        type="INSERT",
        body=dict(
            worker_name=worker_name,
            cpu_core=cpu_core,
            memory=memory_info,
            gpu=gpu_info
        )
    )


def get_updatedata(worker_name, state):
    cpu_usage = get_cpuinfo()["cpu_usage"]
    memory_usage = get_memoryinfo()
    memory_usage = round(memory_usage["memory_usage"] / memory_usage["memory_total"] * 100, 2)
    gpu_proc, gpu_memory, gpu_temp = get_gpuinfo()
    gpu_memory = list(map(lambda x: round(x["gpu_usage"] / x["gpu_total"] * 100, 2), gpu_memory))
    return dict(
        type="UPDATE",
        body=dict(
            worker_name=worker_name,
            state=state,
            usage=dict(
                worker_name=worker_name,
                cpu=cpu_usage,
                memory=memory_usage,
                gpu=gpu_proc,
                gpu_memory=gpu_memory,
                gpu_temp=gpu_temp,
            )
        )
    )


def get_deletedata(worker_name):
    return dict(
        type="DELETE",
        body=dict(
            worker_name=worker_name
        )
    )


def taskstart(task):
    return dict(
        type="TASK_START",
        body=task
    )


def taskend(result):
    return dict(
        type="TASK_END",
        body=result
    )
############################################################


class Worker:

    def __init__(self):
        load_config()
        self.ctx = zmq.asyncio.Context()

        self.worker_name = os.environ.get("WORKER_NAME")
        self.state = "waiting"

        self.works = []

        self.host = os.environ.get("DISTRIBUTOR_HOST")
        self.task_port = int(os.environ.get("TASK_PORT"))
        self.resource_port = int(os.environ.get("RESOURCE_PORT"))
        self.rep_port = int(os.environ.get("DISTRIBUTOR_REP_PORT"))

        try:
            # 최초 연결 시 Distributor에게 알림
            self.req_sock = self.ctx.socket(zmq.REQ)
            self.req_sock.connect(f"tcp://{self.host}:{self.rep_port}")
            self.req_sock.send_json(get_insertdata(self.worker_name))
            self.req_sock.recv()
            # self.req_sock.send_json(get_insertdata(self.worker_name))
            # self.req_sock.recv()

            self.resource_sock = self.ctx.socket(zmq.PUB)
            self.resource_sock.setsockopt(zmq.LINGER, 1)
            self.resource_sock.connect(f"tcp://{self.host}:{self.resource_port}")

            self.task_sock = self.ctx.socket(zmq.SUB)
            self.task_sock.setsockopt_string(zmq.SUBSCRIBE, "")
            self.task_sock.connect(f"tcp://{self.host}:{self.task_port}")
        except OSError:
            print("connection fail")
            exit(1)

    def add_work(self, func):
        self.works.append(func)

    def pre_work(self):
        pass

    def post_work(self):
        pass

    async def send_resource(self):
        with suppress(asyncio.CancelledError):
            while True:
                await self.resource_sock.send_json(get_updatedata(self.worker_name, self.state))
                await asyncio.sleep(1)

    async def process_task(self):
        with suppress(asyncio.CancelledError):
            while True:
                recv_packet = await self.task_sock.recv_json()
                packet_type = recv_packet.get("type", None)
                packet_data = recv_packet.get("body", None)

                if packet_type == "TASK":
                    task_id = packet_data.get("id")
                    worker_name = packet_data.get("worker_name")
                    task_info = packet_data.get("task")
                    if worker_name != self.worker_name:
                        continue

                    for work in self.works:
                        await self.req_sock.send_json({
                            "type": "TASK_START",
                            "body": packet_data
                        })
                        v = await self.req_sock.recv_json()

                        self.state = "running"

                        self.pre_work()
                        ret = work(*task_info) \
                            if type(task_info) is list \
                            else work(**task_info)
                        self.post_work()
                        self.state = "waiting"

                        await self.req_sock.send_json({
                            "type": "TASK_END",
                            "id": task_id,
                            "body": {
                                "worker_name": self.worker_name,
                                "task": packet_data,
                                "result": ret
                            }
                        })
                        v = await self.req_sock.recv_json()

    def run(self):
        try:
            loop = asyncio.get_event_loop()

            tasks = [
                loop.create_task(self.process_task()),
                loop.create_task(self.send_resource())
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
            self.req_sock.send_json(get_deletedata(self.worker_name))
            self.req_sock.recv()
            print("\nexit...")
