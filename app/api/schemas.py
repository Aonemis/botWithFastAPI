from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    artikul: int
    price: float
    rating: float
    all_prod: int

class UserCreate(BaseModel):
    username: str
    password: str
