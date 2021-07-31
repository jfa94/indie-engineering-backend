from typing import List

from conf import db


class ResultsModel(db.Model):
    __tablename__ = 'module_results'

    id = db.Column(db.String(64), primary_key=True)  # Expected to match the awarding platform's certification ID
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_email = db.Column(db.String(254), db.ForeignKey('authentication.email'))
    date_awarded = db.Column(db.DateTime)

    @classmethod
    def find_by_id(cls, _id: str) -> "ResultsModel":
        return cls.query.filter_by(course_id=_id).order_by("date_awarded").first()
    
    @classmethod
    def find_by_email(cls, email: str) -> List["ResultsModel"]:
        return cls.query.filter_by(user_email=email)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

