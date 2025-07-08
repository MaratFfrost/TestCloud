import pytest
import os
import json

PROVIDER_A = "ProviderClientA.json"
PROVIDER_B = "ProviderClientB.json"

EXAMPLE_A = [
    {"provider": "A", "storage_gb": 50, "price_per_gb": 0.05},
    {"provider": "A", "storage_gb": 100, "price_per_gb": 0.03},
    {"provider": "A", "storage_gb": 250, "price_per_gb": 0.025}
]

EXAMPLE_B = [
    {"provider": "B", "storage_gb": 60, "price_per_gb": 0.048},
    {"provider": "B", "storage_gb": 200, "price_per_gb": 0.027},
    {"provider": "B", "storage_gb": 300, "price_per_gb": 0.02}
]


@pytest.fixture(autouse=True)
def setup_and_teardown_files():

    with open(PROVIDER_A, "w") as f:
        json.dump(EXAMPLE_A, f)
    with open(PROVIDER_B, "w") as f:
        json.dump(EXAMPLE_B, f)
    yield
    os.remove(PROVIDER_A)
    os.remove(PROVIDER_B)


@pytest.mark.asyncio
async def test_plans_filter_and_sort(ac):
    resp = await ac.get("/plans?min_storage=100")
    assert resp.status_code == 200
    data = resp.json()

    assert all(item["storage_gb"] >= 100 for item in data)

    costs = [item["storage_gb"] * item["price_per_gb"] for item in data]
    assert costs == sorted(costs)


@pytest.mark.asyncio
async def test_plans_empty_result(ac):
    resp = await ac.get("/plans?min_storage=1000")
    assert resp.status_code == 200
    data = resp.json()
    assert data == []
