from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict

from conf import db

from models.curriculum import CurriculumModel
from models.auth import AuthModel
from schemas.curriculum import CurriculumSchema

ADDED_SUCCESSFULLY = "Course successfully added to curriculum."
UPDATED_SUCCESSFULLY = "Curriculum updated successfully."
DELETED_SUCCESSFULLY = "Course successfully deleted from curriculum."
COURSE_NOT_FOUND = "Unable to locate course id in curriculum."
CURRICULUM_NOT_FOUND = "Unable to locate curriculum."
FORBIDDEN = "Missing necessary permissions."

curriculum_schema = CurriculumSchema()
curriculum_list_schema = CurriculumSchema(many=True)


class EditCurriculum(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user.permissions in ['super', 'admin']:
            curriculum_json = request.get_json()
            curriculum = curriculum_schema.load(curriculum_json, session=db.session)

            curriculum.save_to_db()

            return {"message": ADDED_SUCCESSFULLY}, 201

        return {"message": FORBIDDEN}, 403

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user.permissions in ['super', 'admin']:
            curriculum_json = request.get_json()
            curriculum = CurriculumModel.find_course(curriculum_json["id"])

            if curriculum:
                curriculum.delete_from_db()
                return {"message": DELETED_SUCCESSFULLY}, 410

            return {"message": COURSE_NOT_FOUND}, 404

        return {"message": FORBIDDEN}, 403


class Curriculum(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        request_json = request.get_json()
        curriculum = CurriculumModel.find_by_name(request_json["name"])

        if curriculum:
            return curriculum_list_schema.dump(curriculum), 200

        return {"message": CURRICULUM_NOT_FOUND}, 404
