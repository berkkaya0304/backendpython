from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Sample in-memory data store
data = {
    "1": {"name": "John Doe", "age": 30},
    "2": {"name": "Jane Doe", "age": 25}
}

# API endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(data)

# API endpoint to get a user by ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    if id in data:
        return jsonify(data[id])
    else:
        return jsonify({"error": "User not found"}), 404

# API endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    id = user.get("id")
    if not id:
        # Eğer id yoksa otomatik ata (safety)
        id = str(max([int(k) for k in data.keys()], default=0) + 1)
    data[id] = {
        "name": user["name"],
        "age": user["age"]
    }
    result = data[id].copy()
    result['id'] = id
    return jsonify(result), 201

# API endpoint to update a user
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    if id in data:
        user = request.json
        data[id] = user
        return jsonify(data[id])
    else:
        return jsonify({"error": "User not found"}), 404

# API endpoint to delete a user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    if id in data:
        del data[id]
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
