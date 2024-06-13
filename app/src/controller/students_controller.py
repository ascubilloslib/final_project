from fastapi import HTTPException
from typing import Optional, List
from uuid import UUID
from app.src.models.studentsModel import StudentDB, Student
from app.src.controller.stateless.utils_mapping import pydantic_to_mongo, mongo_to_pydantic, uuid_to_objectid, \
    objectid_to_uuid
from app.src.config.db_settings import db


async def validate_students(student_id: UUID) -> None:

    student = await db.students.find_one({"_id": uuid_to_objectid(student_id), "activate": True})
    if student is None:
        raise HTTPException(status_code=400, detail=f"Student {student_id} does not exist or is not active")


async def validate_subjects(subject_ids: List[UUID]) -> None:
    for subject_id in subject_ids:
        subject = await db.subjects.find_one({"_id": uuid_to_objectid(subject_id), "active": True})
        if subject is None:
            raise HTTPException(status_code=400, detail=f"Subject {subject_id} does not exist or is not active")


async def create_student(student: Student) -> StudentDB:
    if student.subjects:
        await validate_subjects(student.subjects)

    student_doc = pydantic_to_mongo(student)
    result = await db.students.insert_one(student_doc)
    student_doc['id'] = objectid_to_uuid(result.inserted_id)
    return mongo_to_pydantic(StudentDB, student_doc)


async def get_student(student_id: UUID) -> Optional[StudentDB]:
    student_doc = await db.students.find_one({"_id": uuid_to_objectid(student_id), "activate": True})
    if student_doc:
        student_doc['id'] = objectid_to_uuid(student_doc['_id'])
        del student_doc['_id']
        student_doc['subjects'] = [objectid_to_uuid(subject) for subject in student_doc['subjects']]
        return mongo_to_pydantic(StudentDB, student_doc)
    return None


async def list_students() -> List[StudentDB]:
    students = []
    async for student in db.students.find({"activate": True}):
        student['id'] = objectid_to_uuid(student['_id'])
        del student['_id']
        student['subjects'] = [objectid_to_uuid(subject) for subject in student['subjects']]
        students.append(mongo_to_pydantic(StudentDB, student))

    return students


async def update_student(student_id: UUID, update_data: dict) -> bool:
    if 'activate' in update_data:
        del update_data['activate']

    if update_data['subjects']:
        update_data['subjects'] = [uuid_to_objectid(subject_id) for subject_id in update_data['subjects']]

    result = await db.students.update_one(
        {"_id": uuid_to_objectid(student_id), "activate": True}, {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_student(student_id: UUID) -> bool:
    result = await db.students.update_one(
        {"_id": uuid_to_objectid(student_id)},
        {"$set": {"activate": False}}
    )
    return result.modified_count > 0
