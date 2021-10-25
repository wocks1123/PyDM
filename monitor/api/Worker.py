from monitor import monitor_client
from monitor.api import main


@main.route("/workers", methods=["GET"])
def worker_get():
    """
    Worker 목록 반환
    ---
    responses:
      200:
        description: Worker 목록
    """
    return {"data": monitor_client.workers}
