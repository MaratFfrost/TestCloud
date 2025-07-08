import json
from fastapi import APIRouter, HTTPException, Query
import aiofiles
from pydantic import ValidationError
import asyncio

from app.models.pricing_plans import PricingPlan

router = APIRouter(
    tags=["Pricing Plans"],
)


@router.get("/plans", response_model=list[PricingPlan])
async def get_pricing_plans(min_storage: int = Query(0, ge=0)):
    try:
        plan_a, plan_b = await asyncio.gather(
          get_provider("A"), get_provider("B"),
        )
        plans = plan_a + plan_b
        filtered = [
          plan for plan in plans if plan.storage_gb >= min_storage
        ]
        sorted_plans = sorted(
          filtered, key=lambda x: x.storage_gb * x.price_per_gb
        )
        return sorted_plans
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail='invalid files')
    except ValidationError:
        raise HTTPException(status_code=500, detail='invalid data')


async def get_provider(type: str) -> list[PricingPlan]:
    async with aiofiles.open(f"ProviderClient{type}.json") as file:
        content = await file.read()
        data = json.loads(content)
    return [PricingPlan(**plan) for plan in data]
