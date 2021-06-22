from conf import db


class UserModel(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, db.ForeignKey('authentication.id'), primary_key=True)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    joined_date = db.Column(db.DateTime)
    location = db.Column(db.String(64))

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
