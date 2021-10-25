import os
import json
from typing import Union

from DB.Data import Models


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.loads(open('{}/db.json'.format(ROOT_DIR)).read())


class JsonConfig:
    @staticmethod
    def get_data(varname, value=None):
        return DATA.get(varname) or os.environ.get(varname) or value

    @staticmethod
    def set_data(key, value):
        DATA[key] = value
        with open('{}/config.json'.format(ROOT_DIR), 'w') as f:
            json.dump(DATA, f, indent=4)


def get_sql_from_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        ret = f.read().split(";")
        ret.pop()

    return ret


class DBManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.connect()

    def connect(self):
        DB = JsonConfig.get_data('DB', 'sqlite3')
        DB_USER_NAME = JsonConfig.get_data('DB_USER_NAME', 'root')
        DB_USER_PASSWD = JsonConfig.get_data('DB_USER_PASSWD', 'password')
        DB_HOST = JsonConfig.get_data('DB_HOST', 'localhost')
        DB_PORT = JsonConfig.get_data('DB_PORT', 'localhost')
        DB_NAME = JsonConfig.get_data('DB_NAME', 'pydm')
        print("DB", DB)

        if DB == "sqlite3":
            import sqlite3
            self.conn = sqlite3.connect(DB_NAME)
        elif DB == "mysql":
            import pymysql
            self.conn = pymysql.connect(
                user=DB_USER_NAME,
                passwd=DB_USER_PASSWD,
                host=DB_HOST,
                port=DB_PORT,
                db=DB_NAME,
                autocommit=True,
                charset="utf8"
            )

    def get_query_select(self, type_of_class, columns: list = None) -> str:
        query = "SELECT\n\t" + type_of_class._columns
        query += "\nFROM\n\t" + type_of_class._from

        if columns is None:
            return query

        return query

    def query_db(self, query, args=(), one=False):
        cur = self.conn.cursor()
        ret = cur.execute(query, args)
        rv = cur.fetchall()
        # cur.close()
        return (rv[0] if rv else None) if one else rv

    def execute_db(self, query, args=(), many=False):
        cur = self.conn.cursor()

        if many is False:
            ret = cur.execute(query, args)
        else:
            ret = cur.executemany(query, args)
        lastrowid = cur.lastrowid
        self.conn.commit()
        return ret, lastrowid

    def select_by(
            self,
            type_of_class,
            columns: list = None,  # [ col:operator ] ex) id:=
            values: tuple = (),
            one: bool = False
    ):
        query = self.get_query_select(type_of_class, columns)

        if columns is not None:
            query += "\nWHERE\n"
            for c in columns:
                splited = c.split(":")
                col = splited[0]
                operator = splited[1]
                query += f"\t{col}{operator}?\n AND"
            query = query[:-5]

        rows = self.query_db(query, values, one)
        return rows

    def insert_into(self, data: Union[Models, list]) -> Models:
        _data = [data] if type(data) is not list else data

        columns, values = _data[0].get_columns_values()
        query = "INSERT INTO " + type(_data[0]).__name__

        # values의 값이 None이면 삽입 시 default 값으로 지정된다.
        query += "(" + ",".join(columns) + ")"
        query += "\nVALUES(" + ",".join(["?" for _ in range(len(values))]) + ")"

        if type(data) is not list:
            print("query", query)

            ret, lastrowid = self.execute_db(query, values)
            data.id = lastrowid
        else:
            values = []
            for d in _data:
                _, v = d.get_columns_values()
                values.append(v)
            ret, lastrowid = self.execute_db(query, values, many=True)

        return data

    def init_db(self):
        db = self.conn.cursor()

        sqls = get_sql_from_file("scripts/schema.sql")

        for sql in sqls:
            print("sqk", sql)
            db.execute(sql)

    def load_data(self):
        db = self.conn.cursor()

        sqls = get_sql_from_file("scripts/data.sql")
        for sql in sqls:
            db.execute(sql)
