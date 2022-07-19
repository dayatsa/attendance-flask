from app import app
from app.controller import UserController, ActivityController
from flask import request


@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        return UserController.index()
    else:
        return UserController.store()


@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)


@app.route('/login', methods=['POST'])
def login():
    return UserController.login()


@app.route('/activity', methods=['POST', 'GET'])
def activity():
    if request.method == 'GET':
        return ActivityController.index()
    else:
        return ActivityController.store()


@app.route('/activity/<id>', methods=['PUT', 'GET', 'DELETE'])
def activityDetail(id):
    if request.method == 'GET':
        return ActivityController.show(id)
    elif request.method == 'PUT':
        return ActivityController.update(id)
    elif request.method == 'DELETE':
        return ActivityController.delete(id)


@app.route('/refresh', methods=['POST'])
def refresh():
    return UserController.refresh()
        