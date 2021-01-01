from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from flask_login import  UserMixin
import uuid
import datetime

db = SQLAlchemy()



class Users(db.Model,UserMixin):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(80), nullable=True, unique = True)
    email = db.Column(db.String(30), nullable=False, unique = True)
    date_of_joining = db.Column(db.DateTime, default = datetime.datetime.utcnow, nullable = False)
    user_preferences = db.relationship('users_settings', backref="Users")

    def get_id(self):
        return self.uid

class users_settings(db.Model,UserMixin):
    user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uid'),primary_key=True,)
    profile_picture = db.Column(db.TEXT, nullable= True)
    user_backref = db.relationship("Users", backref="usersettings")
    
class rooms(db.Model,UserMixin):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    room_owner = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uid'))
    date_time_created = db.Column(db.DateTime, default = datetime.datetime.utcnow, nullable = False)
    room_name = db.Column(db.String(120), nullable= True)
    links = db.relationship('room_links', backref="rooms")

class room_links(db.Model,UserMixin):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user = db.Column(db.String(50), nullable = False)
    start_date_time = db.Column(db.DateTime, default = datetime.datetime.utcnow, nullable=False)
    short_description = db.Column(db.String(50), nullable = False)
    link = db.Column(db.TEXT, nullable= True)
    in_room =  db.Column(UUID(as_uuid=True), db.ForeignKey('rooms.uid'),primary_key=True)


class users_subscriptions(db.Model,UserMixin):
    just_for_sake_primary_key = db.Column(db.Integer, primary_key = True,autoincrement=True)
    users = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uid'))
    rooms = db.Column(UUID(as_uuid=True), db.ForeignKey('rooms.uid'))



