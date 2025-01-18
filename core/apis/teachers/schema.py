from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from core.models.teachers import Teacher
from marshmallow import Schema, EXCLUDE, fields

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
