from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from constants import users

app = FastAPI()


class SignupRequest(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    age: int
    email: str
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def password_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password do not match")
        return self


class SignupResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


@app.post("/create-user", response_model=SignupResponse, status_code=201)
def create_user(new_user: SignupRequest):
    user = new_user.model_dump()
    name = user["name"]
    user["name"] = name.strip()
    user["id"] = 6
    return user
