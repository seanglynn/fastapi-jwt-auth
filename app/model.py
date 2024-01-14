from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class ClientSchema(BaseModel):
    team_name: str = Field(...)
    client_id: str = Field(...)
    client_secret: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "team_name": "ateam",
                "client_id": "123456789",
                "client_secret": "weaksecret"
            }
        }


class ClientLoginSchema(BaseModel):
    client_id: str = Field(...)
    client_secret: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "client_id": "123456789",
                "client_secret": "weaksecret"
            }
        }
