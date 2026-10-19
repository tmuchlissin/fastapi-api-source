from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/test/items", tags=["Test Items"])


class Item(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


items: dict[int, Item] = {}
next_id = 1


@router.get("/")
def list_items(max_price: float | None = None):
    # Query parameter: GET /test/items/?max_price=20
    if max_price is None:
        return items
    return {item_id: item for item_id, item in items.items() if item.price <= max_price}


@router.get("/{item_id}")
def get_item(item_id: int):
    # Path parameter: GET /test/items/1
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@router.post("/", status_code=201)
def create_item(item: Item):
    # Request body: POST /test/items/ with {"name": "Book", "price": 10}
    global next_id

    item_id = next_id
    items[item_id] = item
    next_id += 1

    return {"id": item_id, "item": item}


@router.put("/{item_id}")
def replace_item(item_id: int, item: Item):
    # Both: item_id is in the path, while item is in the JSON body.
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item
    return {"id": item_id, "item": item}


@router.patch("/{item_id}")
def update_item(item_id: int, update: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = items[item_id].model_copy(
        update=update.model_dump(exclude_unset=True)
    )
    return {"id": item_id, "item": items[item_id]}


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    del items[item_id]
