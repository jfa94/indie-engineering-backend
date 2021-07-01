from conf import ma
from models.curriculum import CurriculumModel


class CurriculumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CurriculumModel
        load_instance = True
        include_fk = True
