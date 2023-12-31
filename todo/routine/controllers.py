import typing as t
from typing import Optional, List
from ellar.common import Controller, ControllerBase, get, put, delete, post
from ellar.common.exceptions import NotFound
from .schemas import TodoSerializer
from .services import TodoServices
#from ..routine.database import engine
from todo.db.models import Todo
#Base.metadata.create_all(bind=engine)


@Controller("/routine")
class TodoController(ControllerBase):
    def __init__(self, todo_service: TodoServices) -> None:
        self.todo_service = todo_service

    @post("/create", response={201: TodoSerializer})
    async def create_todo(self, todo_data: TodoSerializer) -> Todo:
        todo = self.todo_service.add_todo(todo_data)
        return todo

    @put("/{user_id}/{todo_id}", response={200: TodoSerializer})
    async def update(self, todo_id: str, user_id: int, payload: TodoSerializer) -> Optional[TodoSerializer]:
        update_data = payload.dict(exclude_unset=True)
        todo = self.todo_service.update(todo_id, user_id, update_data)
        if not todo:
            raise NotFound("user not found")
        return TodoSerializer.from_orm(todo)

    @get("/status/{user_id}", response={200: t.List[TodoSerializer]})
    async def list_status(self, user_id: int, status_completed: bool) -> List[TodoSerializer]:
        return self.todo_service.list_completed(user_id, status_completed)

    @delete("/{user_id}/{todo_id}", response={204: dict})
    async def delete(self, user_id: int, todo_id: int) -> t.Optional[int]:
        todo = self.todo_service.remove(user_id, todo_id)
        if not todo:
            raise NotFound("User's routine not found")
        return 204, {}

    @get("/all/{user_id}", response={200: t.List[TodoSerializer]})
    async def list(self, user_id: int) -> List[TodoSerializer]:
        return self.todo_service.list(user_id)



