from conf import ma
from models.resource import ResourceModel


class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResourceModel
        load_instance = True
