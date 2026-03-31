from fastapi import FastAPI
from app.routes import auth, users, techs, images, posts

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(techs.router)
app.include_router(images.router)
app.include_router(posts.router)
