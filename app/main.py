from fastapi import FastAPI
import uvicorn

from app.database import Base, engine
from app.routers import products, orders

app = FastAPI()

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Подключение маршрутов
app.include_router(products.router)
app.include_router(orders.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
