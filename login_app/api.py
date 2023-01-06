from . import models, db, app
from flask import request, jsonify, views, Response
from .schema import user_schema, UserSchema
import jwt
from .models import User
from email_validator import validate_email
from .authentication import token_required, requires_permission
from .utils import is_valid
from .services import create_login
import datetime
import os


class RegisterView(views.MethodView):
    def post(self):
        try:
            request_data = request.json
            # validating required/request data.
            schema_errors = user_schema.validate(request_data)
            # print(schema_errors)
            if schema_errors:
                response = jsonify(schema_errors)
                response.status_code = 400
                return response
            rec_emil = request_data['email']
            password = request_data['password']
            if user_schema.validate_password(password):
                return user_schema.validate_password(password)
            # if not is_valid(password):
            #     response = jsonify({"message": "Enter a valid password"})
            #     return response
            ## not working
            # validation = validate_email(rec_emil, check_deliverability=True)
            # rec_emil = validation.email
            user = User.query.filter_by(
                username=request_data['username']).first()
            email = User.query.filter_by(
                email=request_data['email']).first()

            if user is None:
                if email is None:
                    item_obj = user_schema.load(request_data)
                    db.session.add(item_obj)
                    db.session.commit()
                    data = user_schema.dump(request_data)
                    response = jsonify(
                        {"message": "data inserted succusfully", "data": data})
                    response.status_code = 201
                else:
                    response = jsonify({"message": "user is already register"})
            else:
                response = jsonify({"message": "user is already register"})

        except Exception as error:
            response = jsonify({"message": ("Error"), "error": str(error)})
            response.status_code = 400
        return response

    def create():
        create_logic()


class LoginView(views.MethodView):
    def post(self):
        try:
            email = request.json['email']
            password = request.json['password']

            user = User.query.filter_by(email=email).first()
            print(user)
            role = user.role
            if user is not None:
                if user.email == email and user.password == password:

                    token = jwt.encode({'id': user.id, 'role': user.role, 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(hours=24)}, os.environ.get('SIGNING_KEY'), 'HS256')
                    if role == 'admin':
                        response = jsonify(
                            {"message": "admin login succusfull", "token": token})
                    elif role == 'agent':
                        response = jsonify(
                            {"message": "agent login succusfull", "token": token})
                else:
                    response = jsonify(
                        {"message": "incorrect username or password"})
                    response.status_code = 401
        except Exception as error:
            response = jsonify(
                {"message": "error while logging in", "error": str(error)})
            response.status_code = 401
        return response

    @ token_required
    def get(self, current_user):
        try:
            users = User.query.all()
            user_schema = UserSchema(many=True)
            data = user_schema.dump(users)
            response = jsonify(
                {"message": "users fetched succesfully", "data": data})
        except Exception as error:
            response = jsonify(
                {"message": "error while logging in", "error": str(error)})
            response.status_code = 400
        return response


class AdminView(views.MethodView):
    decorators = [requires_permission('admin')]

    def get(self):
        response = jsonify({"message": "welcome to admin"})
        response.status_code = 200
        return response


class AgentView(views.MethodView):
    decorators = [requires_permission('agent')]
    # @requires_permission('agent')

    def get(self):
        response = jsonify({"message": "welcome to agent"})
        response.status_code = 200
        return response
