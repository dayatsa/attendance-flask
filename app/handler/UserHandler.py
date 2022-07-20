from sqlalchemy.exc import OperationalError
from app.model.token_blocklist import TokenBlocklist
from app.model.user import Users
from app import response, db
from app.validator.UserSchema import UserSchema
from flask import request, jsonify
from flask_jwt_extended import *
from datetime import datetime
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


def postUserHandler():
    try:
        schema = UserSchema()

        request_data = request.json
        result = schema.load(request_data)

        name = result['name']
        email = result['email']
        password = result['password']

        user = Users(name=name, email=email)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.ok('success', 'Successfully add user!', data=singleTransform(user), code=201)

    except Exception as e:
        if isinstance(e, ValidationError, OperationalError):
            return response.badRequest('fail', str(e))
        elif isinstance(e, IntegrityError):
            return response.badRequest('fail', e.args)
        else:
            return response.badRequest('fail', str(type(e)))


@jwt_required()
def getUserHandler():
    try:
        user_id = get_jwt_identity()['id']
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return response.badRequest('fail', 'User Not Found')

        data = singleTransform(user)
        return response.ok(status="success", data=data)
    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


@jwt_required()
def putUserHandler():
    try:
        user_id = get_jwt_identity()['id']
        schema = UserSchema()

        request_data = request.json
        result = schema.load(request_data)

        name = result['name']
        email = result['email']
        password = result['password']

        user = Users.query.filter_by(id=user_id).first()
        user.email = email
        user.name = name
        user.setPassword(password)

        db.session.commit()

        return response.ok('success', 'Successfully update user!')

    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


@jwt_required()
def deleteUserHandler():
    try:
        jti = get_jwt()["jti"]
        now = datetime.utcnow()
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        user_id = get_jwt_identity()['id']
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return response.badRequest('fail', 'User not found')

        db.session.delete(user)
        db.session.commit()

        return response.ok('success', 'Successfully delete data!')
    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


def singleTransform(user, withActivity=False):
    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

    if withActivity:
        activity = []
        for i in user.activity:
            activity.append({
                'id': i.id,
                'activity': i.activity,
                'description': i.description,
            })
        data['activity'] = activity

    return data
