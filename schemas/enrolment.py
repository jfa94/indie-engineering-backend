from conf import ma
from models.enrolment import EnrolmentModel


class EnrolmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EnrolmentModel
        load_instance = True
        include_fk = True
