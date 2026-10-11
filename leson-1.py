from fastapi import FastAPI, HTTPException
from constants import users

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello Shyam"}


@app.get("/users/{user_id}")
def get_user(user_id: int):

    for user in users:
        if user["user_id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/search-users")
def search_users(name: str | None = None, limit: int = 2):
    if name is None:
        return users[:limit]

    results = []

    for user in users:
        if user["name"].lower() == name.lower():
            results.append(user)

    if results:
        return results[:limit]

    raise HTTPException(status_code=404, detail="No user found")
