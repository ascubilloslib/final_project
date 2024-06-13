from fastapi import FastAPI
from app.src.routes.student_routes import student_router
from app.src.routes.professor_routes import professor_router
from app.src.routes.subjects_routes import subject_router
app = FastAPI()


app.include_router(student_router)
app.include_router(professor_router)
app.include_router(subject_router)

