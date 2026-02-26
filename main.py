from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.get("/")
def home():
    return {"message": "Hello Deepesh  🚀"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}



@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created",
        "data": user
    }