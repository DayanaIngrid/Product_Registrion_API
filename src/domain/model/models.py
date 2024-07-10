from sqlalchemy import Column, Integer, String, Float, DateTime

from src.config.database import Base, engine
from src.config.database import init_db


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    descricao = Column(String(255))
    preco = Column(Float)
    estoque = Column(Integer)

    def __repr__(self):
        return f'<product(id={self.id}, nome={self.nome}, descricao={self.descricao}, preco={self.preco}, estoque={self.estoque})>'


init_db()
