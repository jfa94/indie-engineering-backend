from typing import List

from conf import db


class ResultsModel(db.Model):
    __tablename__ = 'module_results'

    id = db.Column(db.String(64), primary_key=True)  # Expected to match the awarding platform's certification ID
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    date_awarded = db.Column(db.DateTime)
    verified = db.Column(db.Boolean)

    @classmethod
    def find_by_id(cls, _id: str) -> "ResultsModel":
        return cls.query.filter_by(course_id=_id).order_by("date_awarded").first()
    
    @classmethod
    def find_by_user_id(cls, user_id: int) -> List["ResultsModel"]:
        return cls.query.filter_by(user_id=user_id)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

