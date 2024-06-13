from fastapi import APIRouter
from app.src.models.studentsModel import StudentDB, Student
from app.src.controller.students_controller import create_student, get_student, update_student, delete_student, \
    list_students
from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from fastapi import HTTPException

student_router = APIRouter()


@student_router.post("/students", response_model=StudentDB)
async def create_student_route(student: Student):
    created_student = await create_student(student)
    return created_student


@student_router.get("/students/{student_id}", response_model=StudentDB)
async def get_student_route(student_id: UUID):
    student = await get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@student_router.get("/students", response_model=List[StudentDB])
async def list_students_route():
    students = await list_students()
    return students


@student_router.put("/students/{student_id}", response_model=dict)
async def update_student_route(student_id: UUID, student: Student):
    student_update = student.dict(exclude_unset=True)
    updated = await update_student(student_id, student_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found or not active")
    return JSONResponse(status_code=200, content={"message": "Student successfully updated"})


@student_router.delete("/students/{student_id}", response_model=dict)
async def delete_student_route(student_id: UUID):
    deleted = await delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=204)
