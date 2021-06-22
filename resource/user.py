from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict

from conf import db

from models.user import UserModel
from schemas.user import UserSchema

USER_ALREADY_EXISTS = "User data already exists."
CREATED_SUCCESSFULLY = "User data created successfully."
UPDATED_SUCCESSFULLY = "User data updated successfully."
DELETED_SUCCESSFULLY = "User data deleted successfully."
USER_NOT_FOUND = "Unable to locate user data."

user_schema = UserSchema()


class UserData(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls) -> Tuple[Dict, int]:
        user_json = request.get_json()
        user_json["id"] = get_jwt_identity()
        user = user_schema.load(user_json, session=db.session)

        if UserModel.find_by_id(user.id):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user:
            update_json = request.get_json()
            user_json = user_schema.dump(user)

            for field in update_json:
                user_json[field] = update_json[field]

            user = user_schema.load(user_json, session=db.session)
            user.save_to_db()

            return user_schema.dump(user), 200  # Update to only send a success message?

        return {"message": USER_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def get(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user:
            return user_schema.dump(user), 200

        return {"message": USER_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
            return {"message": DELETED_SUCCESSFULLY}, 410

        return {"message": USER_NOT_FOUND}, 404
