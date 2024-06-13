from pydantic import BaseModel
from typing import Type, TypeVar
from uuid import UUID
from bson import ObjectId, Binary
from bson.binary import UuidRepresentation

T = TypeVar('T', bound=BaseModel)


def pydantic_to_mongo(model: T) -> dict:
    return model.dict(by_alias=True)


# Utility function to convert MongoDB document to Pydantic model
def mongo_to_pydantic(model: Type[T], document: dict) -> T:
    return model(**document)


def uuid_to_objectid(uuid_str: UUID) -> ObjectId:
    return ObjectId(Binary.from_uuid(uuid_str, uuid_representation=UuidRepresentation.STANDARD).hex()[:24])


def objectid_to_uuid(obj_id: ObjectId) -> UUID:
    return UUID(bytes=obj_id.binary + b'\x00\x00\x00\x00')
