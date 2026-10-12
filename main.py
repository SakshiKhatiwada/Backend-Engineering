from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# BASE URL: http://0.0.0.0:8000

@app.get("/")
def read_root():
    return JSONResponse({"Hello": "World"})

@app.get("/students")
def get_students():
    return JSONResponse(
        [
            {
                "name": "Sakshi",
                "roll_num": 29
            },
            {
                "name": "Bini",
                "roll_num": 28
            }
        ]
    )
    
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None
    
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}