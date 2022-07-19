from app.model.activity import Activities as Activities
from flask import request, jsonify
from app import response, db
from app.controller import UserController
from flask_jwt_extended import *


@jwt_required()
def index():
    try:
        id = request.args.get('user_id')
        print("hello ")
        activity = Activities.query.filter_by(user_id=id).all()
        data = transform(activity)
        return response.ok(data, "tes")
    except Exception as e:
        print(e)


def store():
    try:
        activity = request.json['activity']
        desc = request.json['description']
        user_id = request.json['user_id']

        activity = Activities(user_id=user_id, activity=activity, description=desc)
        db.session.add(activity)
        db.session.commit()

        return response.ok('', 'Successfully create activity!')

    except Exception as e:
        print(e)


def update(id):
    try:
        act = request.json['activity']
        desc = request.json['description']
        activity = Activities.query.filter_by(id=id).first()
        activity.activity = act
        activity.description = desc

        db.session.commit()
        print("okeaa")

        return response.ok('', 'Successfully update activity!')

    except Exception as e:
        print(e)


def show(id):
    try:
        activity = Activities.query.filter_by(id=id).first()
        if not activity:
            return response.badRequest([], 'Empty....')

        data = singleTransform(activity)
        return response.ok(data, "")
    except Exception as e:
        print(e)


def delete(id):
    try:
        activity = Activities.query.filter_by(id=id).first()
        if not activity:
            return response.badRequest([], 'Empty....')

        db.session.delete(activity)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        print(e)


def transform(values):
    array = []
    for i in values:
        array.append(singleTransform(i))
    return array


def singleTransform(values):
    data = {
        'id': values.id,
        'user_id': values.user_id,
        'activity': values.activity,
        'description': values.description,
        'created_at': values.created_at,
        'updated_at': values.updated_at,
        'user': UserController.singleTransform(values.users, withActivity=False)
    }

    return data