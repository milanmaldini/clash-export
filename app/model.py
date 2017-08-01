from datetime import datetime, timedelta

from bson.objectid import ObjectId
from mongoengine import DynamicDocument


class Player(DynamicDocument):
    meta = {
        'indexes': [
            'clan.name',
            'clan.tag',
            'name',
            'tag'
        ]
    }


class Clan(DynamicDocument):
    meta = {
        'indexes': [
            'name',
            'tag'
        ]
    }

    @classmethod
    def from_now(cls, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id)

    @classmethod
    def from_now_with_tag(cls, tag, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id, tag=tag)


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)
