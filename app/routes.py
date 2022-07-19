from app import app
from app.handler import ActivityHandler, UserHandler, AuthenticationHandler, AttendanceHandler
from flask import request


@app.route('/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        return UserHandler.getUserHandler()
    elif request.method == 'PUT':
        return UserHandler.putUserHandler()
    elif request.method == 'DELETE':
        return UserHandler.deleteUserHandler()
    else:
        return UserHandler.postUserHandler()


@app.route('/authentications', methods=['POST', 'PUT', 'DELETE'])
def authentications():
    if request.method == 'PUT':
        return AuthenticationHandler.putAuthenticationHandler()
    elif request.method == 'DELETE':
        return AuthenticationHandler.deleteAuthenticationHandler()
    else:
        return AuthenticationHandler.postAuthenticationHandler()


@app.route('/attendance', methods=['GET','POST'])
def attendance():
    if request.method == 'GET':
        return AttendanceHandler.getAttendanceHandler()
    else:
        return AttendanceHandler.postAttendanceHandler()


@app.route('/activity', methods=['POST', 'GET'])
def activity():
    if request.method == 'GET':
        return ActivityHandler.getActivityHandler()
    else:
        return ActivityHandler.postActivityHandler()


@app.route('/activity/<id>', methods=['PUT', 'GET', 'DELETE'])
def activityDetail(id):
    if request.method == 'GET':
        return ActivityHandler.getActivityByIdHandler(id)
    elif request.method == 'PUT':
        return ActivityHandler.putActivityHandler(id)
    elif request.method == 'DELETE':
        return ActivityHandler.deleteActivityHandler(id)
