from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict

from conf import db

from models.results import ResultsModel
from models.auth import AuthModel
from schemas.results import ResultsSchema

RESULTS_ALREADY_EXISTS = "Results data already exists."
CREATED_SUCCESSFULLY = "Results created successfully."
UPDATED_SUCCESSFULLY = "Results updated successfully."
DELETED_SUCCESSFULLY = "Results deleted successfully."
RESULTS_NOT_FOUND = "Unable to locate results."

results_schema = ResultsSchema()
results_list_schema = ResultsSchema(many=True)


class ResultsData(Resource):
    @classmethod
    @jwt_required()
    def post(cls, _id: str) -> Tuple[Dict, int]:
        results_json = request.get_json()
        results_json["course_id"] = int(_id)

        user_id = get_jwt_identity()
        current_user = AuthModel.find_by_id(user_id)
        results_json["user_email"] = current_user.email

        results = results_schema.load(results_json, session=db.session)
        results.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

    @classmethod
    @jwt_required()
    def get(cls, _id: str) -> Tuple[Dict, int]:
        results = ResultsModel.find_by_id(_id)
        return results_schema.dump(results), 200

    @classmethod
    @jwt_required()
    def delete(cls, _id: str) -> Tuple[Dict, int]:
        results = ResultsModel.find_by_id(_id)
        results.delete_from_db()
        return {"message": DELETED_SUCCESSFULLY}, 410


class ResultsList(Resource):
    @classmethod
    @jwt_required()
    def get(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        results = ResultsModel.find_by_user_id(user_id)

        if results:
            return results_list_schema.dump(results), 200

        return {"message": RESULTS_NOT_FOUND}, 404
