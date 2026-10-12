from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class User(BaseModel):
    user_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=30)
    username: str | None = Field(min_length=2, max_length=30, default=None)
    nickname: str | None = Field(default=None, min_length=3, max_length=20)
    age: int = Field(ge=18, le=120)
    email: str = Field(description="The user's contact email")

    @field_validator("name")
    @classmethod
    def name_must_not_be_number(cls, value: str) -> str:
        if any(char.isdigit() for char in value):
            raise ValueError("Name can not contain numbers")
        return value

    @field_validator("username")
    @classmethod
    def username_must_not_contain_whitespace(cls, value: str) -> str:
        if any(char.isspace() for char in value):
            raise ValueError("Username cannot contain whitespace")
        return value


@app.post("/create-user")
def create_user(new_user: User):
    user = new_user.model_dump()
    return user
