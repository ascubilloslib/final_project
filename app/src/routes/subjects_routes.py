from fastapi import APIRouter
from app.src.models.subjectsModel import Subject, SubjectDB
from app.src.controller.subjects_controller import create_subject, get_subject, update_subject, delete_subject, \
    list_subjects
from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from fastapi import HTTPException

subject_router = APIRouter()


@subject_router.post("/subjects/", tags=["Subject"], response_model=SubjectDB)
async def create_subject_route(subject: Subject):
    try:
        created_subject = await create_subject(subject)
        return created_subject
    except ValidationError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@subject_router.get("/subjects/{subject_id}", tags=["Subject"], response_model=SubjectDB)
async def get_subject_route(subject_id: UUID):
    try:
        subject = await get_subject(subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@subject_router.get("/subjects/all/", tags=["Subject"], response_model=List[SubjectDB])
async def list_subjects_route():
    try:
        subjects = await list_subjects()
        return subjects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@subject_router.put("/subjects/{subject_id}", tags=["Subject"], response_model=bool)
async def update_subject_route(subject_id: UUID, subject: Subject):
    try:
        update_data = subject.dict(exclude_unset=True)
        updated = await update_subject(subject_id, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Subject not found or no changes made")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@subject_router.delete("/subjects/{subject_id}", tags=["Subject"], response_model=dict)
async def delete_subject_route(subject_id: UUID):
    try:
        deleted = await delete_subject(subject_id)
        if not deleted:
            return JSONResponse(status_code=404, content={"message": "Subject not found"})
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))