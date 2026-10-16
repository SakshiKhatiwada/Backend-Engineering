from pydantic import BaseModel
# from fastapi import FastAPI

# app = FastAPI()

class Item(BaseModel):
    # id: int
    name: str
    price: float
    is_offer: bool | None = None
    
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name}


item = Item(**{"name": "toothpaste", "price": 142.3, "is_offer": False})
print(item.model_dump())