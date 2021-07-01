from conf import db
from models.curriculum import CurriculumModel

uom_enum = ('YYYY', 'YY', 'MON', 'MONTH', 'MM', 'DY', 'DD', 'HH24', 'HH', 'MI', 'SS')


class CourseModel(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    institution = db.Column(db.String(64))
    platform = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    category = db.Column(db.String(64))
    duration_lower_bound = db.Column(db.Integer)
    duration_upper_bound = db.Column(db.Integer)
    duration_uom = db.Column(db.Enum(*uom_enum))
    effort_lower_bound = db.Column(db.Integer)
    effort_upper_bound = db.Column(db.Integer)
    effort_uom = db.Column(db.Enum(*uom_enum))
    description = db.Column(db.String(512))

    courses = db.relationship("CurriculumModel", uselist=True)

    @classmethod
    def find_by_id(cls, _id: int) -> "CourseModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "CourseModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
