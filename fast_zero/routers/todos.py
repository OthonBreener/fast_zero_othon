from fastapi import APIRouter

from fast_zero.models import Todo
from fast_zero.routers import CurrentUser, T_Session
from fast_zero.schemas import TodoPublic, TodoSchema

router_todos = APIRouter(prefix='/todos', tags=['todos'])


@router_todos.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
