from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request
from typing import Tuple, Dict

from conf import db

from models.course import CourseModel
from models.auth import AuthModel
from schemas.course import CourseSchema

CREATED_SUCCESSFULLY = "Course created successfully."
UPDATED_SUCCESSFULLY = "Course updated successfully."
DELETED_SUCCESSFULLY = "Course deleted successfully."
COURSE_NOT_FOUND = "Unable to locate course."
FORBIDDEN = "Missing necessary permissions."

course_schema = CourseSchema()


class Course(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user.permissions in ['super', 'admin']:
            course_json = request.get_json()
            course = course_schema.load(course_json, session=db.session)

            course.save_to_db()

            return {"message": CREATED_SUCCESSFULLY}, 201

        return {"message": FORBIDDEN}, 403

    @classmethod
    @jwt_required(fresh=True)
    def patch(cls, _id: int) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user.permissions in ['super', 'admin']:
            course = CourseModel.find_by_id(_id)

            if course:
                update_json = request.get_json()
                course_json = course_schema.dump(course)

                for field in update_json:
                    course_json[field] = update_json[field]

                course = course_schema.load(course_json, session=db.session)
                course.save_to_db()

                return course_schema.dump(course), 200  # Update to only send a success message?

            return {"message": COURSE_NOT_FOUND}, 404

        return {"message": FORBIDDEN}, 403

    @classmethod
    @jwt_required()
    def get(cls, _id: int) -> Tuple[Dict, int]:
        course = CourseModel.find_by_id(_id)

        if course:
            return course_schema.dump(course), 200

        return {"message": COURSE_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, _id: int) -> Tuple[Dict, int]:
        user_id = get_jwt_identity()
        user = AuthModel.find_by_id(user_id)

        if user.permissions in ['super', 'admin']:
            course = CourseModel.find_by_id(_id)

            if course:
                course.delete_from_db()
                return {"message": DELETED_SUCCESSFULLY}, 410

            return {"message": COURSE_NOT_FOUND}, 404

        return {"message": FORBIDDEN}, 403
