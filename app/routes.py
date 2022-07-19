from app import app
from app.handler import ActivityController, UserHandler, AuthenticationHandler
from flask import request


@app.route('/users', methods=['POST'])
def users():
    return UserHandler.postUserHandler()


@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserHandler.show(id)
    elif request.method == 'PUT':
        return UserHandler.update(id)
    elif request.method == 'DELETE':
        return UserHandler.delete(id)


@app.route('/authentications', methods=['POST', 'PUT', 'DELETE'])
def authentications():
    if request.method == 'PUT':
        return AuthenticationHandler.putAuthenticationHandler()
    elif request.method == 'DELETE':
        return AuthenticationHandler.deleteAuthenticationHandler()
    else:
        return AuthenticationHandler.postAuthenticationHandler()


@app.route('/activity', methods=['POST', 'GET'])
def activity():
    if request.method == 'GET':
        return ActivityController.getActivityHandler()
    else:
        return ActivityController.postActivityHandler()


@app.route('/activity/<id>', methods=['PUT', 'GET', 'DELETE'])
def activityDetail(id):
    if request.method == 'GET':
        return ActivityController.getActivityByIdHandler(id)
    elif request.method == 'PUT':
        return ActivityController.putActivityHandler(id)
    elif request.method == 'DELETE':
        return ActivityController.deleteActivityHandler(id)



        