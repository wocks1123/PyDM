from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from datetime import datetime

from monitor import db, swagger


ma = Marshmallow()


@swagger.definition("Task")
class Task(db.Model):
    """
    Task Description
    ---
    properties:
      id:
        type: integer
      parameters:
        type: string
      result:
        type: string
      worker_name:
        type: string
      state:
        type: string
      start:
        type: string
      end:
        type: string
    """
    __tablename__ = 'Task'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    parameters = db.Column(db.String(32), nullable=False)
    result = db.Column(db.String(32), nullable=False)
    worker_name = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(8), nullable=False)
    start = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    end = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        datetimeformat = '%Y-%m-%d %H:%M:%S%z'
