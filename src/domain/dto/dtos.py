from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class ProductDTO(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    estoque: int

class ProductCreateDTO(BaseModel):
    nome: str
    descricao: str
    preco: float
    estoque: int

class ProductUpdateDTO(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None

class TokenResponse(BaseModel):
    access_token: str
    expires_at: datetime

class UserTokenDataResponse(BaseModel):
    expires_at: datetime