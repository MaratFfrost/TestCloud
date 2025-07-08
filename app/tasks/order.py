import asyncio
from app.utils.storage import order_storage


async def complete_order_task(order_id: str):
    await asyncio.sleep(25)
    order = order_storage.get(order_id)
    if order:
        order.status = "complete"
        order_storage[order_id] = order
