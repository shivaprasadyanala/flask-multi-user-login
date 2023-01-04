from . import models, db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, validates_schema
import re
from flask import request, jsonify, views, Response


class UserSchema(SQLAlchemyAutoSchema):
    # @validates_schema
    def validate_password(self, passwd):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        # compiling regex
        pat = re.compile(reg)
        # searching regex
        if not re.search(pat, passwd):
            response = jsonify({"message": "Enter a valid password"})
            return response
    username = fields.Str(required=True, validate=[
        validate.Length(min=4, max=250)])
    email = fields.Str(required=True, validate=[
        validate.Length(min=5, max=250)])
    password = fields.Str(required=True, validate=[
        validate.Length(min=8)])

    class Meta:
        model = models.User
        sqla_session = db.Session
        include_fk = True
        load_instance = True


user_schema = UserSchema()
