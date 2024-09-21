from pydantic import BaseModel, ConfigDict, EmailStr


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
