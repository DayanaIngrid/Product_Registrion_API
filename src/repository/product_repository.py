from sqlalchemy.orm import Session
from src.domain.model.models import Product


class ProductRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, description: str, price: float, created_at: datetime):
        product = Product(name=name, description=description, price=price, created_at=created_at)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def read(self, product_id: int):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def update(self, product_id: int, name: str = None, description: str = None, price: float = None):
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if product:
            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if price is not None:
                product.price = price
            self.session.commit()
            self.session.refresh(product)
        return product

    def delete(self, product_id: int):
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if product:
            self.session.delete(product)
            self.session.commit()
        return product

    def find_all(self):
        return self.session.query(Product).all()