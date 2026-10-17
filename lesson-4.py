from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from constants import users

app = FastAPI()


class UserRecord(BaseModel):
    user_id: int
    name: str


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)


class UserReplaceRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)


class UserPatchRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=30)


@app.get("/users", response_model=list[UserRecord])
def get_users(limit: int = 2):
    return users[:limit]


@app.post("/users", status_code=201, response_model=UserRecord)
def create_user(payload: UserCreateRequest):
    id = max([user["user_id"] for user in users]) + 1
    user = payload.model_dump()
    user["user_id"] = id
    return user


@app.put("/users/{user_id}", response_model=UserRecord)
def replace_user(user_id: int, data: UserReplaceRequest):
    for user in users:
        if user["user_id"] == user_id:
            user["name"] = data.name
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.patch("/users/{user_id}", response_model=UserRecord)
def patch_user(user_id: int, payload: UserPatchRequest):
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400, detail="Provide atleast one field to update"
        )

    if "name" in changes and changes["name"] is None:
        raise HTTPException(status_code=422, detail="Name can not be null")

    for user in users:
        if user["user_id"] == user_id:
            user.update(changes)
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["user_id"] == user_id:
            users.remove(user)
            return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
