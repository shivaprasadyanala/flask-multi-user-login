from . import models, db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

def must_not_be_blank(data):
    """
    Validates value must not be blank.
    """
    if data:
        data = data.replace(' ', '')
    if data == '':
        raise ValidationError("Field may not be blank.")
    return data


class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = models.User
        sqla_session = db.Session
        include_fk = True
        load_instance = True


user_schema = UserSchema()
