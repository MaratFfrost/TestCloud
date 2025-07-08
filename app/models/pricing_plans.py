from pydantic import BaseModel, Field


class PricingPlan(BaseModel):
    provider: str = Field(...)
    storage_gb: int = Field(...,  ge=1)
    price_per_gb: float = Field(...,  gt=0)
