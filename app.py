#
# pylint: disable=import-error
#

from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, doc="/swagger", title="User API", description="A Flask API for CRUD operations on users")

# Define the User model
user_model = api.model("User", {
    "id": fields.Integer(readOnly=True, description="The user ID"),
    "name": fields.String(required=True, description="The user name"),
    "email": fields.String(required=True, description="The user email")
})

# In-memory database
users = []
user_id_counter = 1

# Helper function to find user by ID
def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)

# User Resource
@api.route("/users")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return users

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        global user_id_counter
        data = api.payload
        data["id"] = user_id_counter
        users.append(data)
        user_id_counter += 1
        return data, 201

@api.route("/users/<int:user_id>")
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        user = find_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        user = find_user(user_id)
        if not user:
            api.abort(404, "User not found")
        data = api.payload
        user.update(data)
        return user

    def delete(self, user_id):
        """Delete a user"""
        user = find_user(user_id)
        if not user:
            api.abort(404, "User not found")
        users.remove(user)
        return {"message": "User deleted"}, 200

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=8080)


#
# end of file
#

