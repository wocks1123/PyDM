import threading
import os

import zmq

from DM.utils.util import load_config


class MonitorClient:

    def __init__(self, call_ws_send):
        load_config()

        self.send_data = call_ws_send

        self.ctx = zmq.Context()

        self.works = []
        self.worker_info = {}   # key: workername, val: info dict

        self.host = os.environ.get("DISTRIBUTOR_HOST")
        self.monitor_port = int(os.environ.get("MONITOR_PORT"))
        self.rep_port = int(os.environ.get("DISTRIBUTOR_REP_PORT"))

        try:
            # 최초 연결 시 Distributor에게 알림
            self.req_sock = self.ctx.socket(zmq.REQ)
            self.req_sock.connect(f"tcp://{self.host}:{self.rep_port}")
            self.req_sock.send_json({
                "type": "MONITOR",
                "body": "REQ"
            })
            self.workers = self.req_sock.recv_json().get("data")

            self.monitor_sock = self.ctx.socket(zmq.SUB)
            self.monitor_sock.setsockopt_string(zmq.SUBSCRIBE, "")
            self.monitor_sock.connect(f"tcp://{self.host}:{self.monitor_port}")
        except OSError:
            print("connection fail")
            exit(1)

    def process_patcket(self):

        while True:
            packet = self.monitor_sock.recv_json()

            data_type = packet["type"]
            body = packet["body"]


            if data_type == "MONITOR_INIT":
                self.worker_info = body
                self.send_data("MONITOR_INIT", body)
                continue

            if data_type == "INSERT":
                # new_workerlist = body
                worker_name = body["worker_name"]
                self.worker_info[worker_name] = body
                self.send_data("INSERT", body)
                continue

            if data_type == "DELETE":
                worker_name = body["worker_name"]
                del self.worker_info[worker_name]
                self.send_data("DELETE", body)
                continue

            if data_type == "UPDATE":
                self.send_data("UPDATE", body)
                continue

            if data_type == "TASK":
                data = dict(
                    type="TASK",
                    body=body
                )
                self.send_data("TASK", data)
                continue

            if data_type == "TASK_START":
                data = dict(
                    type="TASK_START",
                    body=body
                )
                self.send_data("TASK_START", data)
                continue

            if data_type == "TASK_END":
                data = dict(
                    type="TASK_END",
                    body=body
                )
                self.send_data("TASK_END", data)
                continue

    def run(self):
        self.recv_thread = threading.Thread(target=self.process_patcket)
        self.recv_thread.setDaemon(False)
        self.recv_thread.start()

