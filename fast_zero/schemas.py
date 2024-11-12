from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Message(SchemaBase):
    message: str


class UserSchema(SchemaBase):
    username: str
    email: EmailStr
    password: str


class UserPublic(SchemaBase):
    id: int
    username: str
    email: EmailStr


class Token(SchemaBase):
    access_token: str
    token_type: str


class TodoSchema(SchemaBase):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(SchemaBase):
    todos: list[TodoPublic]


class FilterPage(SchemaBase):
    limit: int = 10
    offset: int = 0


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoUpdate(SchemaBase):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
