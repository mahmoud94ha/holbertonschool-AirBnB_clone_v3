#!/usr/bin/python3
"""
Contains the api app.py
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from flasgger import Swagger, swag_from
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


discription = {
    "flasgger": "0.9.7.1",
    "info": {
        "title": "AirBnB clone - RESTful API",
        "description": "An AirBnB clone",
    }
}
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = \
    '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = \
    '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = \
    '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
swagger = Swagger(app, template=discription)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """main"""
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
