from multiprocessing import AuthenticationError
from app.model.activity import Activities as Activities
from app.validator.ActivitySchema import ActivitySchema
from flask import request
from app import response, db
from app.handler import UserHandler, AttendanceHandler
from flask_jwt_extended import *
from datetime import datetime, date, timedelta
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


@jwt_required()
def getActivityHandler():
    try:
        user = get_jwt_identity()
        id = user['id']
        AttendanceHandler.isCheckin(id)

        if request.json is not None:
            req = request.json['date']
            req = [int(i) for i in req.split('-')]
            date_act = date(req[2], req[1], req[0])
            activity = Activities.query.filter(Activities.user_id==id, Activities.updated_at > date_act, Activities.updated_at < date_act + timedelta(days=1)).all()

        else:
            activity = Activities.query.filter_by(user_id=id).all()
        
        data = transform(activity)
        return response.ok("success", data=data)
    except Exception as e:
        print(e)
        if isinstance(e, AuthenticationError):
            return response.badRequest('fail', str(e))
        else:
            return response.badRequest('fail', str(type(e)))


@jwt_required()
def postActivityHandler():
    try:
        user = get_jwt_identity()

        AttendanceHandler.isCheckin(user['id'])
        schema = ActivitySchema()

        request_data = request.json
        result = schema.load(request_data)

        activity = result['activity']
        desc = result['description']
        user_id = user['id']

        activity = Activities(user_id=user_id, activity=activity, description=desc)
        db.session.add(activity)
        db.session.commit()

        return response.ok('success', 'Successfully create activity!', data=singleTransform(activity), code=201)

    except Exception as e:
        print(e)
        if isinstance(e, (AuthenticationError, ValidationError)):
            return response.badRequest('fail', str(e))
        elif isinstance(e, IntegrityError):
            return response.badRequest('fail', e.args)
        else:
            return response.badRequest('fail', str(type(e)))


@jwt_required()
def putActivityHandler(id):
    try:
        user_id = get_jwt_identity()['id']

        AttendanceHandler.isCheckin(user_id)
        schema = ActivitySchema()
        verifyActivityOwner(id, user_id)

        request_data = request.json
        result = schema.load(request_data)

        act = result['activity']
        desc = result['description']
        updated_at = str(datetime.utcnow())

        activity = Activities.query.filter_by(user_id=user_id, id=id).first()
        activity.activity = act
        activity.description = desc
        activity.updated_at = updated_at

        db.session.commit()

        return response.ok('success', 'Successfully update activity!', data=singleTransform(activity))

    except Exception as e:
        print(e)
        if isinstance(e, (AuthenticationError, ValueError, ValidationError)):
            return response.badRequest('fail', str(e))
        else:
            return response.badRequest('fail', str(type(e)), code=401)


@jwt_required()
def getActivityByIdHandler(id):
    try:
        user_id = get_jwt_identity()['id']
        AttendanceHandler.isCheckin(user_id)

        activity = Activities.query.filter_by(id=id).first()
        if not activity:
            return response.badRequest('fail', 'Activity not found')

        data = singleTransform(activity)
        return response.ok(status="success", data=data)
    except Exception as e:
        print(e)
        if isinstance(e, AuthenticationError):
            return response.badRequest('fail', str(e))
        else:
            return response.badRequest('fail', str(type(e)))


@jwt_required()
def deleteActivityHandler(id):
    try:
        user_id = get_jwt_identity()['id']

        AttendanceHandler.isCheckin(user_id)
        verifyActivityOwner(id, user_id)
        activity = Activities.query.filter_by(id=id).first()

        db.session.delete(activity)
        db.session.commit()

        return response.ok('success', 'Successfully delete data!')
    except Exception as e:
        print(e)
        return response.badRequest('fail', str(e), code=401)
        


def verifyActivityOwner(activity_id, owner_id):
    activity = Activities.query.filter_by(id=activity_id).first()
    if not activity:
        raise ValueError('Activity not found')
    if activity.user_id != owner_id:
        raise AuthenticationError('You are not entitled to access this resource')


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
        'user': UserHandler.singleTransform(values.users, withActivity=False)
    }

    return data