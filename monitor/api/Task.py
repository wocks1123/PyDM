from flask import request

from monitor.api import main
from monitor.model.Task import Task, TaskSchema


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@main.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Task 목록 반환
    ---
    responses:
      200:
        description: Task 목록
        schema:
          $ref: '#definitions/Task'
    """
    t = Task.query.all()
    return tasks_schema.jsonify(t)
