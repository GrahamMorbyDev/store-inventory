from sqlalchemy import create_engine, Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(DATETIME)

    def __repr__(self):
        print(f'Product name: {self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Updated: {self.date_updated}')
