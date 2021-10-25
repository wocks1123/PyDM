import zmq


class Caller:

    @staticmethod
    def call(host, port, *args, **kwargs):
        ctx = zmq.Context()
        req_sock = ctx.socket(zmq.REQ)
        req_sock.connect(f"tcp://{host}:{port}")

        task = {
            'type': 'TASK',
            'body': kwargs
        }
        req_sock.send_json(task)
        ans = req_sock.recv_json()
