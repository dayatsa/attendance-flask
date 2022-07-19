from app.model.user import Users
from app import response, db
from flask import request
from flask_jwt_extended import *
import datetime


def index():
    try:
        users = Users.query.all()
        data = transform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)


def transform(users):
    array = []
    for i in users:
        array.append(singleTransform(i))
    return array


def show(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest([], 'Empty....')

        data = singleTransform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)


def singleTransform(user, withActivity=True):
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


def store():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        user = Users(name=name, email=email)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.ok('', 'Successfully create data!')

    except Exception as e:
        print(e)


def update(id):
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        user = Users.query.filter_by(id=id).first()
        user.email = email
        user.name = name
        user.setPassword(password)

        db.session.commit()

        return response.ok('', 'Successfully update data!')

    except Exception as e:
        print(e)


def delete(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Empty....')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        print(e)

    
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        user = Users.query.filter_by(email=email).first()
        if not user:
            return response.badRequest([], 'Empty....')

        if not user.checkPassword(password):
            return response.badRequest([], 'Your credentials is invalid')

        data = singleTransform(user, withActivity=False)
        expires = datetime.timedelta(hours=1)
        expires_refresh = datetime.timedelta(hours=3)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.ok({
            "data": data,
            "token_access": access_token,
            "token_refresh": refresh_token,
        }, "")
    except Exception as e:
        print(e)


@jwt_refresh_token_required
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return response.ok({
            "token_access": new_token
        }, "")

    except Exception as e:
        print(e)