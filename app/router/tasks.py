from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.model.model import Task
from app.schema.schema import TaskCreateRequest, TaskStatusUpdateRequest, TaskUpdateRequest, TaskResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.depends.depends import require_user_id

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    request: TaskCreateRequest,
    user_id: Annotated[int, Depends(require_user_id)],
    db: AsyncSession = Depends(get_db)
):
    task = Task(
        title=request.title,
        description=request.description,
        user_id=user_id
    )

    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user_id: Annotated[int, Depends(require_user_id)],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )

    return result.scalars().all()


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    user_id: Annotated[int, Depends(require_user_id)],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = request.title
    task.description = request.description

    await db.commit()

    return {"message": "Task updated"}


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    user_id: Annotated[int, Depends(require_user_id)],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()

    return {"message": "Task deleted"}


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def change_status(
    task_id: int,
    request: TaskStatusUpdateRequest,
    user_id: Annotated[int, Depends(require_user_id)],
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = request.status

    await db.commit()
    await db.refresh(task)

    return task