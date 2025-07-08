from pydantic import BaseModel, Field
from uuid import UUID


class OrderCreateRequest(BaseModel):
    provider: str = Field(...,)
    storage_gb: int = Field(..., gt=0)


class OrderResponse(BaseModel):
    order_id: UUID
    status: str


class Order(BaseModel):
    order_id: UUID
    provider: str
    storage_gb: int
    status: str
