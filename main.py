from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI()


class SignupRequest(BaseModel):
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def password_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password do not match")
        return self


@app.post("/create-user")
def create_user(new_user: SignupRequest):
    user = new_user.model_dump()
    return user
