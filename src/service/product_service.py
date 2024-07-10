import logging

from src.domain.dto.dtos import ProductCreateDTO, ProductDTO, ProductUpdateDTO
from src.repository.product_repository import ProductRepository


class ProductService:

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create(self, data: ProductCreateDTO) -> ProductDTO:
        logging.info('Criando um novo produto.')
        product = Product(**data.model_dump())
        try:
            created = self.product_repository.save(product)
            return TypeAdapter(ProductDTO).validate_python(created)
        except IntegrityError as e:
            logging.error(f'Erro ao criar o produto: {data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Produto já existe na base: {e.args[0]}')

    def find_by_id(self, product_id: int) -> ProductDTO:
        logging.info(f'Buscando o produto com ID {product_id}.')
        product = self.product_repository.read(product_id)
        if product is None:
            logging.error(f'Produto com ID {product_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Produto com ID {product_id} não encontrado.')
        return TypeAdapter(ProductDTO).validate_python(product)

    def find_all(self) -> list[ProductDTO]:
        logging.info('Buscando todos os produtos.')
        products = self.product_repository.find_all()
        return [TypeAdapter(ProductDTO).validate_python(product) for product in products]

    def update(self, product_id: int, user_data: ProductUpdateDTO) -> ProductDTO:
        logging.info(f'Atualizando o produto com ID {product_id}.')
        product = self.product_repository.read(product_id)
        if product is None:
            logging.error(f'Produto com ID {product_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Produto com ID {product_id} não encontrado.')

        user_data = user_data.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(product, key, value)
        
        try:
            updated_product = self.product_repository.save(product)
            return TypeAdapter(ProductDTO).validate_python(updated_product)
        except IntegrityError as e:
            logging.error(f'Erro ao atualizar o produto: {user_data}')
            raise HTTPException(status_code=409, detail=f'Erro ao atualizar o produto: {e.args[0]}')

    def delete(self, product_id: int) -> int:
        logging.info(f'Deletando o produto com ID {product_id}.')
        product = self.product_repository.read(product_id)
        if product is None:
            logging.error(f'Produto com ID {product_id} não encontrado.')
            raise HTTPException(status_code=404, detail=f'Produto com ID {product_id} não encontrado.')

        self.product_repository.delete(product)
        logging.info(f'Produto com ID {product_id} deletado.')
        return product_id