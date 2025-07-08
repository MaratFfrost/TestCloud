from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from uuid import uuid4, UUID


from app.models.order import Order, OrderCreateRequest, OrderResponse
from app.utils.storage import order_storage
from app.tasks.order import complete_order_task

router = APIRouter(
    tags=["Orders"],
    prefix="/orders"
)


@router.post("", response_model=OrderResponse,)
async def create_order(
    order: OrderCreateRequest,
    background_tasks: BackgroundTasks
) -> OrderResponse:
    try:
        order_id = uuid4()
        new_order = Order(
          order_id=order_id,
          provider=order.provider,
          storage_gb=order.storage_gb,
          status="pending"
        )

        order_storage[order_id] = new_order

        background_tasks.add_task(complete_order_task, order_id)

        return OrderResponse(
          order_id=order_id,
          status="pending"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse,)
async def get_order_status(order_id: str) -> OrderResponse:
    try:
        order = order_storage.get(UUID(order_id))

        if not order:
            raise HTTPException(status_code=404)

        return OrderResponse(
          order_id=order.order_id,
          status=order.status)

    except HTTPException:
        raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
