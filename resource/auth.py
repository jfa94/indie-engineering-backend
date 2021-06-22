from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict
import hmac

from models.auth import AuthModel
from schemas.auth import AuthSchema
from blocklist import add_to_blocklist

USER_ALREADY_EXISTS = "Email already in use."
CREATED_SUCCESSFULLY = "User created successfully."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User successfully logged out."
DELETED_SUCCESSFULLY = "User deleted successfully."

auth_schema = AuthSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls) -> Tuple[Dict, int]:
        user_json = request.get_json()
        user = auth_schema.load(user_json)

        if AuthModel.find_by_email(user.email):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()

        # TODO: Fix bug with authentication (note: below does not work to log user out)
        jti = get_jwt()["jti"]
        add_to_blocklist(jti)

        user = AuthModel.find_by_id(user_id)
        user.delete_from_db()

        return {"message": DELETED_SUCCESSFULLY}, 410


class UserLogin(Resource):
    @classmethod
    def post(cls) -> Tuple[Dict, int]:
        user_json = request.get_json()
        user_data = auth_schema.load(user_json)

        user = AuthModel.find_by_email(user_data.email)

        if user and hmac.compare_digest(user_data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls) -> Tuple[Dict, int]:
        jti = get_jwt()["jti"]
        add_to_blocklist(jti)
        return {"message": USER_LOGGED_OUT}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls) -> Tuple[Dict, int]:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
