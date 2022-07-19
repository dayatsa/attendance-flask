from json import dumps
from datetime import datetime, timedelta
from app.handler.UserHandler import singleTransform
from app.model.user import Users
from app.model.token_blocklist import TokenBlocklist
from app import response, db, jwt
from app.validator.AuthenticationSchema import AuthenticationSchema
from flask import request
from flask_jwt_extended import *
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


def postAuthenticationHandler():
    try:
        schema = AuthenticationSchema()
        request_data = request.json
        result = schema.load(request_data)
        email = result['email']
        password = result['password']

        user = Users.query.filter_by(email=email).first()
        if not user:
            return response.badRequest('fail', 'User not found', code=401)

        if not user.checkPassword(password):
            return response.badRequest('fail', 'Your credentials is invalid', code=401)

        data = singleTransform(user, withActivity=False)
        expires = timedelta(hours=1)
        expires_refresh = timedelta(hours=3)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.ok(
            "success",
            data={
                "accessToken": access_token,
                "refreshToken": refresh_token,
            },
            code=201
        )
    except Exception as e:
        if isinstance(e, ValidationError):
            return response.badRequest('fail', str(e))
        elif isinstance(e, IntegrityError):
            return response.badRequest('fail', e.args)
        else:
            return response.badRequest('fail', str(type(e)))


@jwt_required(refresh=True)
def putAuthenticationHandler():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return response.ok(
            'success',
            data={
                "accessToken": new_token
            }
        )

    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


@jwt_required()
def deleteAuthenticationHandler():
    try:
        jti = get_jwt()["jti"]
        now = datetime.utcnow()
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        return response.ok('success', 'token revoked')
    except Exception as e:
        print(e)
        return response.badRequest('fail', str(type(e)))


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None
    