import pytest
from uuid import UUID

'''при ручном тестировании отрабатывает этот тест
как надо и есть задержка, а в тестах моментальнон подтверждение
В тестах background-задача может выполниться слишком быстро,
потому что всё работает внутри одного процесса
и одного потока событий => задача не является фоновой'''


@pytest.mark.asyncio
async def test_create_and_check_order_pending(ac):

    response = await ac.post("/orders", json={"provider": "A",
                                              "storage_gb": 100})
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "order_id" in data
    assert data["status"] == "pending"

    order_id = data["order_id"]
    response2 = await ac.get(f"/orders/{order_id}")
    assert response2.status_code == 200


@pytest.mark.asyncio
async def test_order_status_complete_after_delay(ac):

    response = await ac.post("/orders", json={"provider": "A",
                                              "storage_gb": 100})
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    order_id = data["order_id"]

    response2 = await ac.get(f"/orders/{order_id}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["status"] == "complete"


@pytest.mark.asyncio
async def test_order_not_found(ac):

    fake_id = str(UUID(int=1))
    response = await ac.get(f"/orders/{fake_id}")
    assert response.status_code == 404
