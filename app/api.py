from fastapi import FastAPI, Body, Depends, HTTPException

from app.model import PostSchema, ClientLoginSchema, ClientSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT


posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

clients = [ClientSchema(client_id="123456789", client_secret="weaksecret", team_name="ateam")]

app = FastAPI()


# helpers

def check_client(data: ClientLoginSchema):
    for client in clients:
        if client.client_id == data.client_id and client.client_secret == data.client_secret:
            return True
    return False


# route handlers

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }


# @app.post("/client/signup", tags=["client"])
# async def create_client(client: ClientSchema = Body(...)):
#     clients.append(client)  # replace with db call, making sure to hash the password first
#     return signJWT(client.client_id)


@app.post("/client/login", tags=["client"])
async def client_login(client: ClientSchema = Body(...)):
    if check_client(client):
        return signJWT(client.client_id)
    else:
        return HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"}, detail="Wrong login details!")
