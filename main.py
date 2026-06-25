from fastapi import FastAPI
from app.router.users import router as users_router
from app.router.tasks import router as tasks_router

app=FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)