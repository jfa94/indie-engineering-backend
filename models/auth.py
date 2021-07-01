from conf import db
from models.user import UserModel

permission_enum = ('super', 'admin', 'user', 'read')


class AuthModel(db.Model):
    __tablename__ = 'authentication'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    permissions = db.Column(db.Enum(*permission_enum), default='user')
    active = db.Column(db.Enum('true', 'false'), default='true')

    user_data = db.relationship('UserModel', uselist=False, backref='auth', cascade='all, delete')

    @classmethod
    def find_by_email(cls, email: str) -> "AuthModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "AuthModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
