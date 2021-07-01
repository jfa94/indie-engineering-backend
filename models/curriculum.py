from conf import db
from typing import List


class CurriculumModel(db.Model):
    __tablename__ = 'curriculum'

    id = db.Column(db.Integer, primary_key=True)
    certification_name = db.Column(db.String(128), nullable=False, unique=True)
    display_name = db.Column(db.String(128))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    @classmethod
    def find_course(cls, _id: int) -> "CurriculumModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> List["CurriculumModel"]:
        return cls.query.filter_by(certification_name=name).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
