from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import Order, OrderItem, Product
from app.database import get_db
from app.schemas import OrderCreateSchema, OrderUpdateStatusSchema

router = APIRouter()


@router.post("/orders/")
async def create_order(order_data: OrderCreateSchema, db: Session = Depends(get_db)):
    """Создание заказа (POST /orders)"""

    if len(order_data.products) != len(order_data.amounts):
        raise HTTPException(
            status_code=404,
            detail="Список товаров и список их количества должен быть одинаковой длины",
        )

    for product_id, amount_in_order in zip(order_data.products, order_data.amounts):
        product = db.query(Product).filter(Product.id == product_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        # Проверка на достаточное количество товаров на складе
        if amount_in_order > product.amount_all:
            raise HTTPException(
                status_code=400,
                detail=f"Данного количества товара:{product.name} - нет на складе",
            )

    order = Order(status=order_data.status)  # создание нового заказа
    db.add(order)
    db.commit()
    db.refresh(order)

    for product_id, amount_in_order in zip(order_data.products, order_data.amounts):
        product = db.query(Product).filter(Product.id == product_id).first()

        product.amount_all -= amount_in_order  # уменьшение количества товара на складе

        order_item = OrderItem(
            order_id=order.id, product_id=product_id, amount_in_order=amount_in_order
        )

        db.add(order_item)

    db.commit()
    db.refresh(order)

    return {"message": "Заказ успешно создан", "order_id": order.id}


@router.get("/orders/")
async def get_all_orders(db: Session = Depends(get_db)):
    """Получение списка заказов (GET /orders)"""

    orders = db.query(Order).all()
    return orders


@router.get("/orders/{order_id}")
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Получение информации о заказе по id (GET /orders/{id})"""

    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Данный заказ не найден")


@router.patch("/orders/{order_id}/status")
async def update_order_status(
    order_id: int, status_data: OrderUpdateStatusSchema, db: Session = Depends(get_db)
):
    """Обновление статуса заказа (PATCH /orders/{id}/status)"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status_data.status
        db.commit()
        db.refresh(order)
        return order
    raise HTTPException(status_code=404, detail="Данный заказ не найден")
