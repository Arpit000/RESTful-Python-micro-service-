from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Tasks API",
    version="1.0.0",
    description="A small RESTful service for managing tasks.",
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None


class Task(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool
    created_at: datetime


_tasks: dict[UUID, Task] = {}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task_input: TaskCreate) -> Task:
    task = Task(
        id=uuid4(),
        title=task_input.title,
        description=task_input.description,
        completed=False,
        created_at=datetime.now(timezone.utc),
    )
    _tasks[task.id] = task
    return task


@app.get("/api/v1/tasks", response_model=list[Task], tags=["tasks"])
def list_tasks() -> list[Task]:
    return list(_tasks.values())


@app.get("/api/v1/tasks/{task_id}", response_model=Task, tags=["tasks"])
def get_task(task_id: UUID) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/api/v1/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: UUID, task_input: TaskUpdate) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = task.model_copy(update=task_input.model_dump(exclude_unset=True))
    _tasks[task_id] = updated_task
    return updated_task


@app.delete("/api/v1/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: UUID) -> None:
    if _tasks.pop(task_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
