from fastapi import FastAPI, HTTPException

app = FastAPI()

users = [
    {
        "user_id": 123,
        "name": "Shyam",
    },
    {"user_id": 132, "name": "Shyam"},
    {"user_id": 124, "name": "Ram"},
    {"user_id": 125, "name": "Dev"},
    {"user_id": 126, "name": "Kajal"},
]


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
