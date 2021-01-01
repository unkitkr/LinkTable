from flask import Flask, render_template, request, redirect, jsonify, session
from models import db,Users,rooms,users_subscriptions,room_links
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{Your password}@localhost/{Your username}"
app.config['SECRET_KEY'] = '0817PDNTSPA'

db.app = app
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

db.create_all()

@app.route('/', methods = ['GET'])
def homepage():
    return "yaay"

@app.route('/signup', methods = ['POST','GET'])
def signup():
    data =  request.get_json()
    if request.method == 'POST':
        print(data)
        name_ = data['full_name']
        user_email = data['user_email']
        user_password = data['user_password']
        user_name = data['user_name']
        user_email_exist = Users.query.filter_by(email = user_email).first()
        user_name_exist = Users.query.filter_by(user_name = user_name).first()
        if user_email_exist:
            return jsonify({
                'fatal': 'This email is already in use.'
            })
        elif user_name_exist:
            return jsonify({
                'fatal': 'The username is already taken.'
            })
        else:
            new_user = Users(name = name_, email = user_email, password = generate_password_hash(user_password), user_name = user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify({
                    'Success': 'User successfuly added'
                })
            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify({
                    'fatal': 'Database exception occured. Please try again.'
                })
    else:
        return jsonify({
            'fatal' : 'This method is not allowed'
        })

@app.route('/signin', methods = ['GET','POST'])
def signin():
    request.args =  request.get_json()
    if request.method == 'POST':
        user_name = request.args['user_name']
        user_password = request.args['user_password']
        user_exist = Users.query.filter_by(user_name = user_name).first()
        if user_exist:
            if check_password_hash(user_exist.password, user_password):
                login_user(user_exist)
                return jsonify({
                    'success':'You loggedin successfully'
                }), 200
            return jsonify({
                'fatal':'Incorrect password'
            })
        return jsonify({
            'fatal': 'Wrong username'
        })
    else:
        return jsonify({
            'fatal':'Wrong method'
        })



@app.route('/getuserdata', methods = ['GET'])
def current_user_data():
    if request.method == 'GET':
        if current_user.is_authenticated:
            user_id = current_user.uid
            rooms_owned = rooms.query.filter_by(room_owner = user_id).all()
            rooms_joined_data = users_subscriptions.query.filter_by(users = user_id).all()
            rooms_joined_data = [{'room':x.rooms} for x in rooms_joined_data]
            rooms_created_data = [{'room_id':x.uid} for x in rooms_owned]
            session['rooms_joined'] = [x['room'] for x in rooms_joined_data]
            session['rooms_owned'] = [x['room_id'] for x in rooms_created_data]
            print(session)
            user_data = {
                'name': current_user.name,
                'username':current_user.user_name,
                'email': current_user.email,
                'user_rooms_owned': rooms_created_data,
                'rooms_joined': rooms_joined_data
            }
            return jsonify(user_data)
        else:
            return jsonify({
                'fatal':"You're not authenticated"
            })
    else:
        return jsonify({
            'fatal':'Method not allowed'
        })


@app.route('/createroom', methods = ['POST'])
def create_room():
    if request.method == 'POST':
        if current_user.is_authenticated:
            user_id = current_user.uid
            request.args = request.get_json()
            room_name = request.args['room_name']
            new_room = rooms(room_name = room_name, room_owner = user_id)
            try:
                db.session.add(new_room)
                db.session.commit()
                return jsonify({
                    'Success': 'Room created successfuly.'
                })
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'fatal': 'Database exception occured. Please try again.'
                })
        else:
            return jsonify({
                'fatal':"You're not authenticated"
            })
    else:
        return jsonify({
            'fatal':'Method not allowed'
        })


@app.route('/sendlink', methods = ['POST'])
def send_link():
    if request.method == 'POST':
        if current_user.is_authenticated:
            link = request.args['link']
            room = uuid.UUID(request.args['room_id']) 
            description = request.args['link_description']
            if room in session['rooms_joined'] or room in session['rooms_owned']:
                new_link = room_links(user = current_user.uid, short_description = description,link = link, in_room = room )
                try:
                    db.session.add(new_link)
                    db.session.commit()
                    return jsonify({
                        'Success': 'link posted created successfuly.'
                    })
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    return jsonify({
                        'fatal': 'Database exception occured. Please try again.'
                    })
            else:
                return jsonify({
                    'fatal':"You've not joined the room"
                })
        else:
            return jsonify({
                'fatal':"You're not authenticated"
            })
    else:
        return jsonify({
            'fatal':'Method not allowed'
        }) 

  
@app.route('/getroomdata', methods = ['GET','POST'])
def get_room_data():   
    if request.method == 'GET':
        if current_user.is_authenticated:
            room = uuid.UUID(request.args['room_id'])
            if room in session['rooms_joined'] or room in session['rooms_owned']:
                all_links = room_links.query.filter_by(in_room = room).all() 
                all_users = users_subscriptions.query.filter_by(rooms = room).all()
                all_users = [x.users for x in all_users]
                link_data = [{
                    'sent_by': all_link.user,
                    'link': all_link.link,
                    'link_description': all_link.short_description,
                    'sent_date' : all_link.start_date_time,
                    'message_id': all_link.uid,
                } for all_link in all_links]
                return jsonify({
                    'messages': link_data,
                    'users': all_users,
                })
            else:
                return jsonify({
                    'fatal':"You've not joined the room"
                })
        else:
            return jsonify({
                'fatal':"You're not authenticated"
            })
    else:
        return(jsonify({
            'fatal':'Method not allowed'
        }))
    


 
@app.route('/joinroom', methods = ['GET','POST'])
def join_room():
    if current_user.is_authenticated:
        if request.method == 'POST':
            user_id = current_user.uid
            room_id = uuid.UUID(request.args['room_id'])
            if (room_id in session['rooms_joined'] or room_id in session['rooms_created'] ):
                return jsonify({
                    'fatal':"You're already subscribed"
                })
            else:
                new_subscription = users_subscriptions(users = user_id, rooms = room_id)
                try:
                    db.session.add(new_subscription)
                    db.session.commit()
                    return jsonify({
                        'Success': 'Subscription added successfuly.'
                    })
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    return jsonify({
                        'fatal': 'Database exception occured. Please try again.'
                    })
        else:
            return jsonify({
                'fatal':"You're not authenticated"
            })
    else:
        return jsonify({
            'fatal':'Method not allowed'
        })



@app.route('/logout', methods = ['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({
            'success': 'Logged out'
        })
    else:
        return jsonify({
                'fatal':"You're not authenticated"
            })


if __name__ == '__main__':
    app.run(debug=True)
