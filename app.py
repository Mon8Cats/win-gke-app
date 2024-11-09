# pylint: disable=import-error
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # The URL pointing to the API definition

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Flask API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# In-memory "database"
users = []

# Helper function to find user by ID
def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)

# Create a new user (POST /users)
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(user)
    return jsonify(user), 201

# Get all users (GET /users)
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# Get a single user by ID (GET /users/<user_id>)
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200

# Update a user by ID (PUT /users/<user_id>)
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])

    return jsonify(user), 200

# Delete a user by ID (DELETE /users/<user_id>)
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = find_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
