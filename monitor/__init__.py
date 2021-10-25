import os

from flask import Flask, request
from flasgger import Swagger, swag_from
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


from .config import env_config


socket_io = SocketIO(
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
)
db = SQLAlchemy()
ma = Marshmallow()
swagger = Swagger()


from monitor.MonitorClient import MonitorClient

# Worker 정보 실시간으로 웹소켓을 통해 전송
def send_workers_info(path, data):
    print("Path", path)
    socket_io.emit(path, data, broadcast=True)


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "templates")

monitor_client = MonitorClient(
    send_workers_info
)


def create_app(config_name):
    app = Flask(
        __name__, 
        instance_relative_config=True,
        static_url_path='', 
        static_folder=STATIC_PATH,
    )

    app.config.from_object(env_config[config_name])
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .api import main as api_blueprint
    from .view import view as view_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(view_blueprint)

    CORS(app)
    socket_io.init_app(app)
    swagger.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        monitor_client.run()

    return app


