from fastapi import FastAPI
from stm_api.users.controllers import router as users_router

app = FastAPI(
    title="Simple Task Manager API",
    description="A simple API for managing users's scoped tasks",
    version="1.0.0"
)

app.include_router(users_router)


@app.get("/", tags=["Home page"])
async def homepage():
    return {"message": "Welcome to the Simple Task Manager API !"}