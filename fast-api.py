from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel

#definig the base model for the data validation using pydantic library
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

#initializing the app
app = FastAPI()

# Initial list of items
itm_lst = [
    {"name": "Pencil", "price": 5.0, "brand": "Octane"},
    {"name": "Pen", "price": 10.0, "brand": "Octane"},
    {"name": "Copy", "price": 45.0, "brand": "Octane"}
]

"""To fetch the time we use GET {url}/items"""
@app.get('/items', response_model=List[Item])
def get_items():
    return itm_lst


    """ To get item by their name in path url use {url}/items/item_name

    Raises:
        HTTPException: 404 Not found    
    """
@app.get('/items/{name}', response_model=Item)
def get_item_by_name(name: str = Path(..., description="The name of the item to retrieve")):
    for item in itm_lst:
        if item['name'] == name:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    """To add item to the list mention the item json in the body and post.
        POST {url}/items
        Body: {
        "name":"item_name",
        "price":"item_price",
        "brand":"item_brans"
        }
    Raises:
        HTTPException: 400 Bad request
    """

@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    if any(i['name'] == item.name for i in itm_lst):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    new_item = {"name": item.name, "price": item.price, "brand": item.brand}
    itm_lst.append(new_item)
    return new_item

    """For updating the item
        PUT {url}/items
        body:{}
    Raises:
        HTTPException: 404 Not found    
    """

@app.put('/items', response_model=Item)
def update_item(item: Item):
    for i, existing_item in enumerate(itm_lst):
        if existing_item['name'] == item.name:
            itm_lst[i] = {"name": item.name, "price": item.price, "brand": item.brand}
            return itm_lst[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/items/{name}', response_model=Item)
def delete_item(name: str = Path(..., description="The name of the item to delete")):
    for i, item in enumerate(itm_lst):
        if item['name'] == name:
            deleted_item = itm_lst.pop(i)
            return deleted_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
