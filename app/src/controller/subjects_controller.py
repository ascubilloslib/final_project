from fastapi import HTTPException
from typing import Optional, List
from uuid import UUID
from app.src.models.subjectsModel import Subject, SubjectDB
from app.src.controller.stateless.utils_mapping import pydantic_to_mongo, mongo_to_pydantic, uuid_to_objectid, \
    objectid_to_uuid

from app.src.controller.students_controller import validate_students
from app.src.config.db_settings import db


async def validate_subject(subject_id: UUID) -> None:
    subject = await db.subjects.find_one({"_id": uuid_to_objectid(subject_id), "active": True})
    if subject is None:
        raise HTTPException(status_code=400, detail=f"Subject {subject_id} does not exist or is not active")


async def create_subject(subject: Subject) -> SubjectDB:
    if subject.students:
        for student_id in subject.students:
            await validate_students(student_id)

    subject_doc = pydantic_to_mongo(subject)
    subject_doc['group_id'] = uuid_to_objectid(subject_doc['group_id'])
    subject_doc['professor_id'] = uuid_to_objectid(subject_doc['professor_id'])
    result = await db.subjects.insert_one(subject_doc)

    subject_doc['id'] = objectid_to_uuid(result.inserted_id)
    return mongo_to_pydantic(SubjectDB, subject_doc)


async def get_subject(subject_id: UUID) -> Optional[SubjectDB]:
    subject_doc = await db.subjects.find_one({"_id": uuid_to_objectid(subject_id), "active": True})
    if subject_doc:
        subject_doc['id'] = objectid_to_uuid(subject_doc['_id'])
        del subject_doc['_id']
        subject_doc['students'] = [objectid_to_uuid(student) for student in subject_doc['students']]
        return mongo_to_pydantic(SubjectDB, subject_doc)
    return None


async def list_subjects() -> List[SubjectDB]:
    subjects = []
    async for subject in db.subjects.find({"active": True}):
        subject['id'] = objectid_to_uuid(subject['_id'])
        del subject['_id']
        subject['students'] = [objectid_to_uuid(student) for student in subject['students']]
        subjects.append(mongo_to_pydantic(SubjectDB, subject))
    return subjects


async def update_subject(subject_id: UUID, update_data: dict) -> bool:
    if 'active' in update_data:
        del update_data['active']

    if 'students' in update_data:
        for student_id in update_data['students']:
            await validate_students(student_id)
        update_data['students'] = [uuid_to_objectid(student_id) for student_id in update_data['students']]

    result = await db.subjects.update_one(
        {"_id": uuid_to_objectid(subject_id), "active": True}, {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_subject(subject_id: UUID) -> bool:
    result = await db.subjects.update_one(
        {"_id": uuid_to_objectid(subject_id)},
        {"$set": {"active": False}}
    )
    return result.modified_count > 0
