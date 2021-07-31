from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict

from conf import db

from models.enrolment import EnrolmentModel
from models.auth import AuthModel
from schemas.enrolment import EnrolmentSchema

CREATED_SUCCESSFULLY = "Enrolment created successfully."
UPDATED_SUCCESSFULLY = "Enrolment updated successfully."
DELETED_SUCCESSFULLY = "Enrolment deleted successfully."
ENROLMENT_NOT_FOUND = "Unable to locate enrolment."
USER_NOT_FOUND = "Unable to locate user."
FORBIDDEN = "Missing necessary permissions."

enrolment_schema = EnrolmentSchema()
enrolment_list_schema = EnrolmentSchema(many=True)


class EnrolmentData(Resource):
    @classmethod
    @jwt_required()
    def post(cls, _id: int) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user:
            enrolment_json = request.get_json()
            enrolment_json["curriculum_id"] = _id
            enrolment_json["user_email"] = user.email
            enrolment = enrolment_schema.load(enrolment_json)
            enrolment.save_to_db()

            return {"message": CREATED_SUCCESSFULLY}, 201

        return {"message": USER_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def patch(cls, _id: int) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user:
            enrolment = EnrolmentModel.find_by_id(_id)

            if enrolment.user_email == user.email:
                update_json = request.get_json()
                enrolment_json = enrolment_schema.dump(enrolment)

                for field in update_json:
                    enrolment_json[field] = update_json[field]

                enrolment = enrolment_schema.load(enrolment_json, session=db.session)
                enrolment.save_to_db()

                return enrolment_schema.dump(enrolment), 200

            return {"message": ENROLMENT_NOT_FOUND}, 404

        return {"message": USER_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def get(cls, _id: int) -> Tuple[Dict, int]:
        enrolment = EnrolmentModel.find_by_id(_id)

        if enrolment:
            return enrolment_schema.dump(enrolment), 200

        return {"message": ENROLMENT_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def delete(cls, _id: int) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)
        enrolment = EnrolmentModel.find_by_id(_id)

        if enrolment.user_email == user.email:
            enrolment.delete_from_db()
            return {"message": DELETED_SUCCESSFULLY}, 410

        return {"message": ENROLMENT_NOT_FOUND}, 404


class EnrolmentList(Resource):
    @classmethod
    @jwt_required()
    def get(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        enrolment_list = EnrolmentModel.find_by_email(user.email)
        if enrolment_list:
            return enrolment_list_schema.dump(enrolment_list), 200

        return {"message": ENROLMENT_NOT_FOUND}, 404
