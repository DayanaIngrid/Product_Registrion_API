from sqlalchemy.orm import Session
from src.domain.model.models import Product
from datetime import datetime


from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, product):
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def find_by_id(self, product_id: int):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def find_all(self):
        return self.session.query(Product).all()

    def update(self, product_id: int, product_data):
        product = self.find_by_id(product_id)
        if product:
            for key, value in product_data.dict().items():
                setattr(product, key, value)
            self.session.commit()
            self.session.refresh(product)
            return product
        return None

    def delete(self, product_id: int):
        product = self.find_by_id(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            return True
        return False
