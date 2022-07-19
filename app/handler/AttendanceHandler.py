from multiprocessing import AuthenticationError
from app.model.attendance import Attendance as Attendance
from flask import request
from app import response, db
from app.handler import UserHandler
from flask_jwt_extended import *
from datetime import datetime


@jwt_required()
def getAttendanceHandler():
    try:
        user_id = get_jwt_identity()['id']

        attend = Attendance.query.filter_by(user_id=user_id).all()        
        data = transform(attend)
        return response.ok("success", data=data)
    except Exception as e:
        print(e)


@jwt_required()
def postAttendanceHandler():
    try:
        user_id = get_jwt_identity()['id']
        print(user_id, datetime.utcnow().date())
        check_attendance = Attendance.query.filter(Attendance.user_id==user_id, Attendance.checkin_at > datetime.utcnow().date()).first()

        if check_attendance is None:
            '''check in'''
            check_in = datetime.utcnow()
            attend = Attendance(user_id=user_id, checkin_at=check_in, checkout_at=None)        
            db.session.add(attend)
            db.session.commit()
            return response.ok('success', 'Successfully check in!', code=201)

        elif check_attendance.checkout_at is None:
            '''check out'''
            check_attendance.checkout_at = datetime.utcnow()    
            db.session.add(check_attendance)
            db.session.commit()
            return response.ok('success', 'Successfully check out!', code=201)

        else:
            '''already check out'''
            return response.badRequest('fail', 'you have checked in and checkout today')

    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


def isCheckin(user_id):
    check_attendance = Attendance.query.filter(Attendance.user_id==user_id, Attendance.checkin_at > datetime.utcnow().date()).first()
    if check_attendance is None:
        raise AuthenticationError('Please check in first') 


def transform(values):
    array = []
    for i in values:
        array.append(singleTransform(i))
    return array


def singleTransform(values):
    data = {
        'id': values.id,
        'user_id': values.user_id,
        'checkin_at': values.checkin_at,
        'checkout_at': values.checkout_at,
        'user': UserHandler.singleTransform(values.users, withActivity=False)
    }

    return data