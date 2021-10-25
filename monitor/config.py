import os
import json


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.loads(open('{}/db.json'.format(ROOT_DIR)).read())


class JsonConfig:
    @staticmethod
    def get_data(varname, value=None):
        return DATA.get(varname) or os.environ.get(varname) or value

    @staticmethod
    def set_data(key, value):
        DATA[key] = value
        with open('{}/db.json'.format(ROOT_DIR), 'w') as f:
            json.dump(DATA, f, indent=4)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USER_NAME = JsonConfig.get_data('DB_USER_NAME', 'root')
    DB_USER_PASSWD = JsonConfig.get_data('DB_USER_PASSWD', 'password')
    DB_HOST = JsonConfig.get_data('DB_HOST', 'localhost')
    DB_PORT = JsonConfig.get_data('DB_HOST', 3306)
    DB_NAME = JsonConfig.get_data('DB_NAME', 'pydm')
    DB = JsonConfig.get_data('DB', 'sqlite')

    @staticmethod
    def get_database_uri():
        if Config.DB == "sqlite3":
            return f"sqlite:///{Config.DB_NAME}"
        elif Config.DB == "sqlite":
            return f"mysql+pymysql://{Config.DB_USER_NAME}:{Config.DB_USER_PASSWD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
        else:
            raise Exception("Unavailable DB...")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
