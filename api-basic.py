from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure secret key in production
jwt = JWTManager(app)

# Mock database of items
items = [
    {"name": "Green Apple", "price": 160},
    {"name": "Momos", "price": 120}
]

# Mock user data (in a real application, this should be fetched from a database)
users = {
    "admin": "admin"
}

# Login endpoint to authenticate users and generate JWT
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username = auth_data.get('username', None)
    password = auth_data.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# Protected routes using JWT
@app.route('/items/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_item(name):
    item = next((i for i in items if i['name'] == name), None)
    if item:
        items.remove(item)
        return jsonify({"msg": "Item deleted successfully"}), 200
    return jsonify({"msg": "Item not found"}), 404

@app.route('/items/<string:name>', methods=['GET'])
@jwt_required()
def get_item(name):
    item = next((i for i in items if i['name'] == name), None)
    if item:
        return jsonify({"item": item}), 200
    return jsonify({"msg": "Item not found"}), 404

@app.route('/items', methods=['PUT'])
@jwt_required()
def update_item():
    request_data = request.get_json()
    item = next((i for i in items if i['name'] == request_data['name']), None)
    if item:
        item['price'] = request_data['price']
        return jsonify({"msg": "Item updated successfully"}), 200
    return jsonify({"msg": "Item not found"}), 204

@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    return jsonify({"items": items}), 200

@app.route('/items', methods=['POST'])
@jwt_required()
def add_item():
    request_data = request.get_json()
    new_item = {
        "name": request_data['name'],
        "price": request_data['price']
    }
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == "__main__":
    app.run()
