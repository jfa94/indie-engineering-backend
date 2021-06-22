from conf import ma
from models.auth import AuthModel


class AuthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthModel
        load_only = ("password",)
        load_instance = True
