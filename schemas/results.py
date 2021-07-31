from conf import ma
from models.results import ResultsModel


class ResultsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultsModel
        load_instance = True
        include_fk = True
