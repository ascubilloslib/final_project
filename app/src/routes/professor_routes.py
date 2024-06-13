from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from uuid import UUID
from typing import List

from app.src.models.professorModel import Professor, ProfessorDB

from app.src.controller.professor_controller import create_professor, get_professor, update_professor, list_professors, \
    delete_professor

professor_router = APIRouter()


@professor_router.post("/professor/", tags=["Professor"], response_model=ProfessorDB)
async def create_professor_route(professor: Professor):
    try:
        created_student = await create_professor(professor)
    except ValidationError as err:
        raise HTTPException(status_code=404, detail=str(err))
    return created_student


@professor_router.get("/professors/{professor_id}", tags=["Professor"], response_model=ProfessorDB)
async def get_professor_route(professor_id: UUID):
    professor = await get_professor(professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@professor_router.get("/professors/all/", tags=["Professor"], response_model=List[ProfessorDB])
async def list_professors_route():
    professors = await list_professors()
    return professors


@professor_router.put("/professors/{professor_id}", tags=["Professor"], response_model=bool)
async def update_professor_route(professor_id: UUID, professor: Professor):
    update_data = professor.dict(exclude_unset=True)
    updated = await update_professor(professor_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Professor not found")
    return updated


@professor_router.delete("/professors/{professor_id}", tags=["Professor"], response_model=dict)
async def delete_professor_route(professor_id: UUID):
    deleted = await delete_professor(professor_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"message": "Professor not found"})
    return Response(status_code=204)