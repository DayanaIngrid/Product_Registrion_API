from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.dependencies import get_authenticated_product, get_product_service
from src.config.database import get_db
from src.domain.dto.dtos import ProductCreateDTO, ProductUpdateDTO, ProductDTO
from src.service.product_service import ProductService
from src.repository.product_repository import ProductRepository

product_router = APIRouter(prefix='/products', tags=['Products'], dependencies=[Depends(get_authenticated_product)])

@product_router.post('/', status_code=201, description='cria um novo produto', response_model=ProductCreateDTO)
async def create(request: ProductCreateDTO, product_service: ProductService = Depends(get_product_service)):
    return product_service.create(request)

@product_router.get('/{product_id}', status_code=200, description='Buscar produto por ID', response_model=ProductDTO)
async def find_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)):
    return product_service.find_by_id(product_id = product_id)


@product_router.get('/', status_code=200, description='Buscar todos os produtos', response_model=list[ProductDTO])
async def find_all(product_service: ProductService = Depends(get_product_service)):
    return product_service.find_all()

@product_router.put('/{product_id}', status_code=200, description='Atualizar um produto', response_model=ProductUpdateDTO)
async def update_product(product_id: int, product_data: ProductUpdateDTO, product_service: ProductService = Depends(get_product_service)):
    return product_service.update(product_id, product_data)

@product_router.delete('/{product_id}', status_code=204, description='Deletar usuário por ID')
async def delete_product(product_id: int, product_service: ProductService = Depends(get_product_service)):
    return product_service.delete(product_id)
