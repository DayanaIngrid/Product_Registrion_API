from fastapi import APIRouter, Depends

from src.config.dependencies import get_authenticated_product, get_product_service
from src.config.database import get_db
from src.domain.dto.dtos import ProductCreateDTO, ProductUpdateDTO, ProductDTO
from src.service.product_service import ProductService
from src.repository.product_repository import ProductRepository

product_router = APIRouter(prefix='/products', tags=['Products'], dependencies=[Depends(get_authenticated_product)])


def get_product_repo(session: Session = Depends(get_db)):
    return ProductRepository(session=session)


@product_router.post('/', status_code=201, description='Cria um novo produto', response_model=ProductDTO)
async def create_product(
        request: ProductCreateDTO,
        product_repo: ProductRepository = Depends(get_product_repo),
        authorization: str = Depends(get_authenticated_product)
):
    product_service = ProductService(product_repo)
    return product_service.create(data=request)


@product_router.get('/{id}', status_code=200, description='Buscar produto por ID', response_model=ProductDTO)
async def find_product_by_id(id: int, product_repo: ProductRepository = Depends(get_product_repo),
                             authorization: str = Depends(get_authenticated_product)):
    product_service = ProductService(product_repo)
    return product_service.find_by_id(product_id=id)


@product_router.get('/', status_code=200, description='Buscar todos os produtos', response_model=list[ProductDTO])
async def find_all_products(product_repo: ProductRepository = Depends(get_product_repo),
                            authorization: str = Depends(get_authenticated_product)):
    product_service = ProductService(product_repo)
    return product_service.find_all()


@product_router.put('/{id}', status_code=200, description='Atualizar um produto', response_model=ProductDTO)
async def update_product(id: int, product_data: ProductUpdateDTO, product_repo: ProductRepository = Depends(get_product_repo),
                         authorization: str = Depends(get_authenticated_product)):
    product_service = ProductService(product_repo)
    return product_service.update(product_id=id, user_data=product_data)


@product_router.delete('/{id}', status_code=204, description='Deletar produto por ID')
async def delete_product(id: int, product_repo: ProductRepository = Depends(get_product_repo),
                         authorization: str = Depends(get_authenticated_product)):
    product_service = ProductService(product_repo)
    product_service.delete(product_id=id)