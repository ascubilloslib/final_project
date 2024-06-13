from bson import ObjectId
from pydantic import BaseModel
from typing import Optional, Type, TypeVar, Any, List
from uuid import UUID
from app.src.models.professorModel import ProfessorDB,Professor
from app.src.controller.stateless.utils_mapping import pydantic_to_mongo, mongo_to_pydantic, objectid_to_uuid, uuid_to_objectid
from app.src.config.db_settings import db

T = TypeVar('T', bound=BaseModel)


async def create_professor(professor: Professor) -> ProfessorDB:
    professor_doc = pydantic_to_mongo(professor)
    result = await db.professors.insert_one(professor_doc)
    professor_doc['id'] = objectid_to_uuid(result.inserted_id)
    return mongo_to_pydantic(ProfessorDB, professor_doc)


async def get_professor(professor_id: UUID) -> ProfessorDB:
    professor_id = uuid_to_objectid(professor_id)
    result = await db.professors.find_one({"_id": professor_id, "activate": True})

    if result:
        result['id'] = objectid_to_uuid(result['_id'])
        del result['_id']
        return mongo_to_pydantic(ProfessorDB, result)


async def list_professors() -> List[ProfessorDB]:
    professors = []
    async for professor in db.professors.find({"activate": True}):
        professor['id'] = objectid_to_uuid(professor['_id'])
        professors.append(mongo_to_pydantic(ProfessorDB, professor))
    return professors


async def update_professor(professor_id: UUID, professor_data: dict) -> bool:
    professor_id = uuid_to_objectid(professor_id)

    if 'activate' in professor_data:
        del professor_data['activate']

    result = await db.professors.update_one(
        {"_id": professor_id, "activate": True}, {"$set": professor_data}
    )
    return result.modified_count > 0


async def delete_professor(professor_id: UUID) -> bool:
    professor_id = uuid_to_objectid(professor_id)
    result = await db.professors.update_one(
        {"_id": professor_id},
        {"$set": {"activate": False}}
    )
    return result.modified_count > 0

