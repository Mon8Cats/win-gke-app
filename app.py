# pylint: disable=import-error
from flask import Flask, jsonify
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

# Sample API endpoint
@app.route("/api/user", methods=["GET"])
def get_user():
    return jsonify({"name": "John", "email": "john@example.com"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)