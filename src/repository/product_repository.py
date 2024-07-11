from sqlalchemy.orm import Session
from src.domain.model.models import Product
from datetime import datetime


class ProductRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product ):
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product):
        self.session.delete(product)
        self.session.commit()
    
    def read(self, product_id: int):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def find_all(self):
        return self.session.query(Product).all()