from app.model.user import Users
from app import response, db
from app.validator.UserSchema import UserSchema
from flask import request, jsonify
from flask_jwt_extended import *


# def index():
#     try:
#         users = Users.query.all()
#         data = transform(users)
#         return response.ok(data, "")
#     except Exception as e:
#         print(e)


# def transform(users):
#     array = []
#     for i in users:
#         array.append(singleTransform(i))
#     return array


# def show(id):
#     try:
#         users = Users.query.filter_by(id=id).first()
#         if not users:
#             return response.badRequest([], 'Empty....')

#         data = singleTransform(users)
#         return response.ok(data, "")
#     except Exception as e:
#         print(e)


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
        return response.badRequest('fail', str(type(e)))



@jwt_required()
def putUserByIdHandler(id):
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        user = Users.query.filter_by(id=id).first()
        user.email = email
        user.name = name
        user.setPassword(password)

        db.session.commit()

        return response.ok('', 'Successfully update user!')

    except Exception as e:
        print(e)


@jwt_required()
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
