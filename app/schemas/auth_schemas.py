from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    organization_name: str
    branch_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
