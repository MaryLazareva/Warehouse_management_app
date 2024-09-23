from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models import Product
from app.database import get_db
from app.schemas import ProductCreateSchema, ProductUpdateSchema

router = APIRouter()


@router.post("/products/")
async def create_product(product_data: ProductCreateSchema,db: Session = Depends(get_db),):
    """Создание товара (POST /products)"""

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        amount_all=product_data.amount_all,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/")
async def get_all_products(db: Session = Depends(get_db)):
    """Получение списка товаров (GET /products)"""

    products = db.query(Product).all()
    if products:
        return products
    raise HTTPException(status_code=404, detail="Нет ни одного товара")


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получение информации о товаре по id (GET /products/{id})"""

    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    raise HTTPException(status_code=404, detail="Данный товар не найден")


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    db: Session = Depends(get_db),
):
    """Обновление информации о товаре (PUT /products/{id})"""

    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.amount_all = product_data.amount_all
        db.commit()
        db.refresh(product)
        return product
    raise HTTPException(status_code=404, detail="Данный товар не найден")


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Удаление товара (DELETE /products/{id})"""
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Продукт удален"}
    raise HTTPException(status_code=404, detail="Данный товар не найден")
