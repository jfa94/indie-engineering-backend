from conf import ma
from models.course import CourseModel


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CourseModel
        load_instance = True
