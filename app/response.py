from flask import jsonify, make_response


def ok(status, message='', data='', code=200):
    if data == '':
        res = {
            'status': status,
            'message': message
        }
    elif message == '':
        res = {
            'status': status,
            'data': data
        } 
    else:
        res = {
            'status': status,
            'message': message,
            'data': data
        }

    return make_response(jsonify(res)), code


def badRequest(status, message, code=400):
    res = {
        'status': status,
        'message': message
    }

    return make_response(jsonify(res)), code