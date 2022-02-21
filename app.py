from sqlalchemy import create_engine, Column, Integer, String, FLOAT, DATETIME
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///inventory.db', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(FLOAT)
    date_updated = Column(DATETIME)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
