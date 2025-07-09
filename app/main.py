from fastapi import FastAPI
import redis.asyncio as aioredis
from contextlib import asynccontextmanager

from app.api.orders import router as router_orders
from app.api.pricing_plans import router as pricing_plans_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = "redis://redis:6379"
    try:
        r = aioredis.from_url(redis_url)
        await r.ping()
        print("Redis connected successfully!")
        app.state.aioredis = r
        yield
    except Exception as e:
        print(f"Redis connection failed: {e}")
    finally:
        await r.aclose()

app = FastAPI(
    title="Cloud Storage Marketplace",
    description="Marketplace for aggregated storage pricing plans",
    version="0.1",
    lifespan=lifespan
)


app.include_router(router_orders)
app.include_router(pricing_plans_router)
