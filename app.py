from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError
from dotenv import load_dotenv
import os

from conf import db, ma
from blocklist import get_blocklist
from resource.auth import UserRegister, UserLogin, UserLogout, TokenRefresh
from resource.results import ResultsData, ResultsList
from resource.user import UserData
from resource.course import Course

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

api = Api(app)

jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    blocklist = get_blocklist()
    return jwt_data["jti"] in blocklist


# Authentication resources
# NOTE: passwords are stored as-received, ensure hashed before posting
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

# User data resources
api.add_resource(UserData, "/user")

# Course resources
api.add_resource(Course, "/course", "/course/<int:_id>")

# Results resources
api.add_resource(ResultsData, "/result/<int:_id>")
api.add_resource(ResultsList, "/results")


if __name__ == '__main__':
    app.run(port=5000)
