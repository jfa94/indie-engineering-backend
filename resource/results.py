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

results_schema = resultsSchema()


class ResultsData(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls) -> Tuple[Dict, int]:
        results_json = request.get_json()
        results_json["id"] = get_jwt_identity()
        results = results_schema.load(results_json, session=db.session)

        if resultsModel.find_by_id(results.id):
            return {"message": results_ALREADY_EXISTS}, 400

        results.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls) -> Tuple[Dict, int]:
        results_id = get_jwt_identity()
        results = resultsModel.find_by_id(results_id)

        if results:
            update_json = request.get_json()
            results_json = results_schema.dump(results)

            for field in update_json:
                results_json[field] = update_json[field]

            results = results_schema.load(results_json, session=db.session)
            results.save_to_db()

            return results_schema.dump(results), 200  # Update to only send a success message?

        return {"message": results_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    def get(cls) -> Tuple[Dict, int]:
        results_id = get_jwt_identity()
        results = resultsModel.find_by_id(results_id)

        if results:
            return results_schema.dump(results), 200

        return {"message": results_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls) -> Tuple[Dict, int]:
        results_id = get_jwt_identity()
        results = resultsModel.find_by_id(results_id)

        if results:
            results.delete_from_db()
            return {"message": DELETED_SUCCESSFULLY}, 410

        return {"message": results_NOT_FOUND}, 404
