"""
Data.py
===
- 데이터 베이스의 데이터를 표현하는 클래스
- 테이블의 데이터를 1대1 매칭
- 클래스 구성법
  - @database, @sql_helper 순으로 데코레이터 지정
  - Models 클래스 상속
  - 클래스 이름은 Table의 이름과 동일하게 정의
  - 멤버 변수는 Table의 column
    - 타입: INT -> int, VARCHAR -> str, DATE -> datetime

TODO
- JOIN 구현 미흡
"""

from dataclasses import dataclass, asdict
from datetime import datetime


def _proc(cls, tables, fields):
    if tables is not None:
        anno = {}
        for table in tables:
            attrs = table.__dict__.get("__annotations__", {})
            for k, v in attrs.items():
                if k not in anno:
                    anno[k] = v
        setattr(cls, "__annotations__", anno)

    props = cls.__dict__["__annotations__"]


    _from = ""
    if fields is not None:
        a_name = tables[0].__name__
        b_name = tables[1].__name__
        cast_a = f"_{a_name}"
        cast_b = f"_{b_name}"

        _from += f"{a_name} as {cast_a}"
        _from += f"\n\tINNER JOIN {b_name} as {cast_b}"
        _from += f"\n\tON {cast_a}.{fields[0]} = {cast_b}.{fields[1]}"
    else:
        _from += cls.__name__

    if fields is not None:
        a_columns = tables[0].__dict__["__annotations__"]
        b_columns = tables[1].__dict__["__annotations__"]

        cols = []
        for c in a_columns:
            cols.append(f"{cast_a}.{c} as {c}")
        for c in b_columns:
            if c != fields[1]:
                cols.append(f"{cast_b}.{c} as {c}")
    else:
        cols = props

    _columns = ",\n\t".join(cols)

    setattr(cls, "_columns", _columns)
    setattr(cls, "_from", _from)

    return cls


def sql_helper(_cls=None, *, tables: list = None, fields: list = None):
    def _wrap(cls):
        setattr(cls, "__tables", tables)
        return _proc(cls, tables, fields)

    if _cls is None:
        return _wrap

    return _wrap(_cls)


class Models:
    def get_columns_values(self):
        props = self.__dict__

        columns = []
        values = []
        for c in props:
            if props[c] is None:
                continue

            columns.append(c)
            values.append(props[c])
        values = tuple(values)

        return columns, values

    def to_dict(self):
        return asdict(self)


@sql_helper
@dataclass
class Task(Models):
    id: int = None
    parameters: str = None
    result: str = None
    worker_name: str = None
    state: str = None
    start: datetime = None
    end: datetime = None
