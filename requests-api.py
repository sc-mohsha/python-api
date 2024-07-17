import requests

BASE_URL = "http://127.0.0.1:8080"

# Define the endpoints
endpoints = {
    "get_items": f"{BASE_URL}/items",
    "get_item_by_name": f"{BASE_URL}/items/{{name}}",
    "create_item": f"{BASE_URL}/items",
    "update_item": f"{BASE_URL}/items",
    "delete_item": f"{BASE_URL}/items/{{name}}"
}

# fetching all the items
response = requests.get(endpoints["get_items"])
print("Items get",response.json())

print("\n" "\n")

# fetching item by their name
name = "Pencil"
response = requests.get(endpoints["get_item_by_name"].format(name=name))
print("This is the detail of that item" ,response.json())

# Adding the items
new_item = {
    "name": "Eraser",
    "price": 3.0,
    "brand": "Stationery"
}
print("\n" "\n")
response = requests.post(endpoints["create_item"], json=new_item)
print("Item is added")

