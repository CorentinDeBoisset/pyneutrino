from sqlalchemy.engine import ScalarResult
from typing import Sequence


def serialize_obj(obj, attributes: list):
    return {attr: getattr(obj, attr) for attr in attributes}


def serialize_list(objs: list, attributes: list):
    # We skip None values since sqlalchemy's ScalarResult can have None (at the end of a sequence usually)
    return [serialize_obj(obj, attributes) for obj in objs if obj is not None]


def serialize(source, attributes: list):
    if isinstance(source, ScalarResult):
        return serialize_list(list(source.all()), attributes)

    if isinstance(source, Sequence):
        return serialize_list(source, attributes)

    return serialize_obj(source, attributes)
