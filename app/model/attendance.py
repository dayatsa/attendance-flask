from app import db
from app.model.user import Users


class Attendance(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    checkin_at = db.Column(db.DateTime, index=True)
    checkout_at = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey(Users.id))
    users = db.relationship("Users", backref="user_attendance_id")

    def __repr__(self):
        return '<Attendance {}>'.format(self.id)