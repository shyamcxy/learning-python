from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    user_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=30)
    nickname: str | None = Field(default=None, min_length=3, max_length=20)
    age: int = Field(ge=18, le=120)
    email: str = Field(description="The user's contact email")


@app.post("/create-user")
def create_user(new_user: User):
    user = new_user.model_dump()
    return user
