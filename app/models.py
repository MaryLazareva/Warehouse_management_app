from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount_all = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(DateTime, default= datetime.now().replace(microsecond=0))  # возвращение текущей даты и времени
    status = Column(String, nullable=False)


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    amount_in_order = Column(Integer, nullable=False)
