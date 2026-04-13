from pydantic import BaseModel, Field
from typing import Literal


class Message(BaseModel):
    message: str


class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
    expires_in: int


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: Literal["todo", "in_progress", "blocked", "done"] = "todo"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    due_date: str | None = None


class TaskUpdate(BaseModel):
    id: str
    title: str
    description: str = ""
    status: Literal["todo", "in_progress", "blocked", "done"] = "todo"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    due_date: str | None = None
    done: bool = False


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: str
    due_date: str | None = None
    done: bool
    created_at: str
    updated_at: str


class TaskList(BaseModel):
    tasks: list[TaskResponse]