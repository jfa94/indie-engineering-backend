from conf import db, ma
from typing import List
from datetime import datetime


class BlockedJWTModel(db.Model):
    __tablename__ = 'blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False, unique=True)
    datetime_added = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def find_all(cls) -> List["BlockedJWTModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class BlockedJWTSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlockedJWTModel
        load_instance = True


def get_blocklist() -> List[str]:
    blocklist_schema = BlockedJWTSchema(many=True)
    blocklist = blocklist_schema.dump(BlockedJWTModel.find_all())
    return [blocked["jti"] for blocked in blocklist]


def add_to_blocklist(jti: str) -> None:
    blocked_jwt_schema = BlockedJWTSchema()
    blocked_jwt = blocked_jwt_schema.load({"jti": jti}, session=db.session)
    blocked_jwt.save_to_db()
