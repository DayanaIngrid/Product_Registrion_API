import logging
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from src.domain.dto.dtos import ProductCreateDTO, ProductDTO, ProductUpdateDTO
from src.repository.product_repository import ProductRepository
from src.domain.model.models import Product

class ProductService:

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create(self, product_data: ProductCreateDTO) -> ProductDTO:
        logging.info('Criando um novo produto.')
        product = Product(**product_data.model_dump())
        try:
            created = self.product_repository.create(product)
            return TypeAdapter(ProductDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar o produto: {product_data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Produto já existe na base: {e.args[0]}')
    
    
    def read(self, product_id: int) -> ProductDTO:
        logging.info('Buscando um produto.')
        return TypeAdapter(ProductDTO).validate_python(self._read(product_id))

    def _read(self, product_id: int) -> Product:
        product = self.product_repository.read(product_id)
        if product is None:
            logging.error(f'Produto {product_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Produto {product_id} não encontrado.')
        return product

    def find_all(self) -> list[ProductDTO]:
        logging.info('Buscando todos os produtos.')
        products = self.product_repository.find_all()
        return [TypeAdapter(ProductDTO).validate_python(product) for product in products]

    def update(self, product_id: int, product_data: ProductUpdateDTO):
        logging.info(f'Atualizando o produto {product_id}.')
        product = self._read(product_id)
        product_data = product_data.model_dump(exclude_unset=True)
        for key, value in product_data.items():
            setattr(product, key, value)
        updated_product = self.product_repository.create(product)
        logging.info(f'Produto {product_id} atualizado: {updated_product}')
        return TypeAdapter(ProductDTO).validate_python(updated_product)

    def delete(self, product_id: int) -> int:
        product = self._read(product_id)
        self.product_repository.delete(product)
        logging.info(f'Produto {product_id} deletado')
        return product_id