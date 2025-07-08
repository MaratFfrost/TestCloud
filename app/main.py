from fastapi import FastAPI

from app.api.orders import router as router_orders
from app.api.pricing_plans import router as pricing_plans_router

app = FastAPI(
    title="Cloud Storage Marketplace",
    description="Marketplace for aggregated storage pricing plans",
    version="0.1"
)

app.include_router(router_orders)
app.include_router(pricing_plans_router)
