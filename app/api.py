from fastapi import FastAPI, Body, Depends, HTTPException
import os
import json
from dotenv import load_dotenv

from app.model import PostSchema, ClientLoginSchema, ClientSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

# Load environment variables from .env file
load_dotenv()

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]


app = FastAPI()


# Check if client credentials are valid
def check_client(data: ClientLoginSchema) -> bool:
    clients = get_clients()
    for client in clients:
        if client.client_id == data.client_id and client.client_secret == data.client_secret:
            return True
    return False


class ClientsNotConfigured(Exception):
    pass


def get_clients() -> list[ClientSchema]:
    clients_config_json = os.getenv("CLIENTS_CONFIG")
    if clients_config_json:
        clients_config = json.loads(clients_config_json)
        # Process the expected clients and validate schema
        clients = [ClientSchema(**client) for client in clients_config]
        print(clients)  # Just for demonstration
        return clients
    else:
        raise ClientsNotConfigured("Clients config not found! Be sure to define CLIENTS_CONFIG in the .env file.")


@app.on_event("startup")
async def load_config():
    get_clients()



##################################
# Sample code from testdriven.io
##################################
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}


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


##################################
# Sample code from testdriven.io
##################################


@app.post("/client/login", tags=["client"])
async def client_login(client: ClientSchema = Body(...)):
    # Validate client against expected list
    if check_client(client):
        return signJWT(client.client_id)
    else:
        return HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"}, detail="Wrong login details!")
