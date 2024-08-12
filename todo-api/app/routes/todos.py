from datetime import datetime, timezone
from fastapi import APIRouter, Response, status
from sqlalchemy import select, update
from pydantic import BaseModel

from ..database.session import SessionDep
from ..database.models import Todo as TodoModel
from ..utils import utc_now


router = APIRouter()


class _Todo(BaseModel):
    id: int
    title: str
    content: str
    is_done: bool


class GetAllResponse(BaseModel):
    data: list[_Todo]

@router.get("")
def get_all(session: SessionDep) -> GetAllResponse:
    todos = session.scalars(
        select(TodoModel).where(
            TodoModel.deleted_at.is_(None)
        )
    ).all()

    return GetAllResponse(
        data=[
            _Todo(
                id=item.id,
                title=item.title,
                content=item.content,
                is_done=item.is_done,
            )
            for item in todos
        ]
    )


# ---


class GetItemResponse(BaseModel):
    data: _Todo

@router.get("/{id}")
def get_item(id: str, response: Response, session: SessionDep) -> GetItemResponse:
    todo = session.scalar(select(TodoModel).where(TodoModel.id == id))

    if todo is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return GetItemResponse(
        data=_Todo(
            id=todo.id,
            title=todo.title,
            content=todo.content,
            is_done=todo.is_done,
        )
    )


# ---


class CreateItemPayload(BaseModel):
    title: str
    content: str

class CreateItemResponse(BaseModel):
    data: _Todo

@router.post("")
def create_item(
    session: SessionDep,
    payload: CreateItemPayload,
) -> CreateItemResponse:
    item = TodoModel(
        title=payload.title,
        content=payload.content,
        is_done=False
    )

    session.add(item)
    session.flush()

    return CreateItemResponse(
        data=_Todo(
            id=item.id,
            title=item.title,
            content=item.content,
            is_done=item.is_done,
        )
    )


# ---


class PatchItemPayload(BaseModel):
    title: str | None = None
    content: str | None = None
    is_done: bool | None = None

class PatchItemResponse(BaseModel):
    data: _Todo

@router.patch("/{id}")
def patch_item(
    id: str,
    session: SessionDep,
    response: Response,
    payload: PatchItemPayload,
) -> PatchItemResponse:
    todo = session.scalar(select(TodoModel).where(TodoModel.id == id))

    if todo is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    update_data = payload.model_dump(exclude_unset=True)

    item = _Todo(
        id=todo.id,
        title=todo.title,
        content=todo.content,
        is_done=todo.is_done,
    ).model_copy(update=update_data)

    session.execute(
        update(TodoModel)
        .where(TodoModel.id == id)
        .values(
            title=item.title,
            content=item.content,
            is_done=item.is_done,
        )
    )
    session.flush()

    return PatchItemResponse(
        data=item
    )


# ---


@router.delete("/{id}")
def delete_item(id: int, session: SessionDep):
    todo = session.scalar(select(TodoModel).where(TodoModel.id == id))
    if todo is None:
        return

    todo.deleted_at = utc_now()
    session.flush()
    return
