from conf import db


class EnrolmentModel(db.Model):
    __tablename__ = "enrolment"

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(254), db.ForeignKey('authentication.email'))
    curriculum_id = db.Column(db.Integer, db.ForeignKey('curriculum.id'))
    enrolment_date = db.Column(db.DateTime)
    certified = db.Column(db.Boolean, default=False)
    certification_date = db.Column(db.DateTime)

    @classmethod
    def find_by_id(cls, _id: int) -> "EnrolmentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "EnrolmentModel":
        return cls.query.filter_by(user_email=email)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
