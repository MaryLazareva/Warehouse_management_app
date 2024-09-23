from fastapi.testclient import TestClient
from app.main import app

# Создание клиента для тестирования
client = TestClient(app)


def test_create_produc():
    """Тест создания товара"""
    
    response = client.post(
        "/products/",
        json={
            "name": "Тестовый товар",
            "description": "Описание",
            "price": 100.0,
            "amount_all": 50,
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Тестовый товар"
    assert response.json()["description"] == "Описание"
    assert response.json()["price"] == 100.0


def test_get_product_by_id():
    """Тест получения товара по его id"""

    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_product():
    """Тест удаления товара"""

    response = client.post(
        "/products/",
        json={
            "name": "Удаляемый товар",
            "description": "Описание",
            "price": 100.0,
            "amount_all": 50,
        },
    )
    product_id = response.json()["id"]

    # Удаление товара
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Продукт удален"

    # Попытка получения удалённого товара (должно вернуться 404)
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_update_product():
    """Тест обновления товара"""

    response = client.post(
        "/products/",
        json={
            "name": "Обновляемый товар",
            "description": "Описание",
            "price": 500.0,
            "amount_all": 5,
        },
    )

    product_id = response.json()["id"]

    # Обновление товара
    update_response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Обновленный товар",
            "description": "Описание после обновления",
            "price": 200.0,
            "amount_all": 7,
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 200.0
    assert update_response.json()["description"] == "Описание после обновления"

def test_get_all_products():
    """Тест на получения списка всех товаров"""

    client.post("/products/", json={
        "name": "Товар 1",
        "description": "Описание 1",
        "price": 400.0,
        "amount_all": 15
    })

    client.post("/products/", json={
        "name": "Товар 2",
        "description": "Описание 2",
        "price": 300.0,
        "amount_all": 10
    })

# Получение списка всех продуктов
response = client.get("/products/")

assert response.status_code == 200
assert isinstance(response.json(), list)
assert len(response.json()) >= 2

def test_create_order_with_sufficient_quantity_of_goods():
    """Тест создания заказа при достаточном количестве товара"""

    response = client.post(
        "/orders/", json={"status": "в процессе", "products": [5], "amounts": [1]}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Заказ успешно создан"


def test_create_order_with_insufficient_of_goods():
    """Тест создания заказа при недостаточном количестве товара"""

    response = client.post(
        "/orders/", json={"status": "в процессе", "products": [1], "amounts": [1000]}
    )
    assert response.status_code == 400
    assert f"Данного количества товара" in response.json()["detail"]


def test_get_order_by_id():
    """Тест получения заказа по id"""

    response = client.get("/orders/18")

    assert response.status_code == 200
    assert response.json()["id"] == 18


def test_get_all_orders():
    """Тест на получение всех заказов"""

    product_1 = client.post("/products/", json={
        "name": "Товар 3",
        "description": "Описание 3",
        "price": 400.0,
        "amount_all": 15
    }).json()

    product_2 = client.post("/products/", json={
        "name": "Товар 4",
        "description": "Описание 4",
        "price": 300.0,
        "amount_all": 10
    }).json()

    # Созданрие нового заказа
    client.post("/orders/", json={
        "status": "в процессе",
        "products": [product_1["id"], product_2["id"]],
        "amounts": [5, 5]
    })

    get_all_orders = client.get("/orders/")

    assert get_all_orders.status_code == 200
    assert isinstance(get_all_orders.json(), list)
    assert len(get_all_orders.json()) >= 1

