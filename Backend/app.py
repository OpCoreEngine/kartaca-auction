import datetime
import os
from dotenv import load_dotenv
from functools import wraps
import jwt
import redis
from flask import Flask, request, jsonify, redirect, url_for, session, abort, current_app
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_sqlalchemy import SQLAlchemy
import bcrypt

if os.environ.get('ENV') == 'docker':
    print("running from docker, so don't load environment variables from local .env file")
else:
    print("running from local, so load environment variables from local .env file")
    load_dotenv('../.env')

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False, engineio_logger=True, logger=True)

products = [
    {"id": 1, "name": "1. Ürün", "price": 100},
    {"id": 2, "name": "2. Ürün", "price": 200},
    {"id": 3, "name": "3. Ürün", "price": 300},
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


def hash_password(password, secret_key):
    salt = bcrypt.hashpw(secret_key.encode('utf-8'), bcrypt.gensalt())
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(hashed_password, entered_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token yok!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            session['username'] = data['username']
        except:
            return jsonify({'message': 'Token geçersiz!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/get_username', methods=['GET'])
@token_required
def get_username():
    return jsonify({"username": session['username']})


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    entered_password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password(user.password, entered_password):
        token = jwt.encode(
            {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify(status='success', token=token)
    return jsonify(status='error', message='Kullanıcı adı ya da şifre hatalı')


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')      
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(status='error', message='Kullanıcı adı kullanımda')
    hashed_password = hash_password(password, current_app.config['SECRET_KEY'])
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(status='success', message='Kayıt başarılı')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/products', methods=['GET'])
@token_required
def get_products():
    app.logger.debug("Inside get_products() function")
    return jsonify(products)


@socketio.on('join_products')
def on_join_products():
    room = 'products'
    join_room(room)


@socketio.on('leave_products')
def on_leave_products():
    room = 'products'
    leave_room(room)


@socketio.on('bid')
def on_bid(data):
    product_id = data['product_id']
    new_price = data['new_price']
    app.logger.debug("product_id: %s")
    for product in products:
        if product['id'] == product_id:
            product['price'] = new_price
            break
    emit('update_price', {"product_id": product_id, "new_price": new_price, "last_bidder": data["last_bidder"]},
         broadcast=True)


@app.route('/bid/<int:product_id>', methods=['POST'])
@token_required
def bid(product_id):
    try:
        increment = request.json.get("increment", 10)
        username = session['username']
        product = [p for p in products if p["id"] == product_id][0]
        product["price"] += int(increment)
        product["last_bidder"] = username
        return jsonify({"success": True, "new_price": product["price"], "last_bidder": username})
    except Exception as e:
        app.logger.error("Error in bid(): %s", e)
        abort(500)


@app.route('/token_validation', methods=['POST'])
@token_required
def token_validation():
    return jsonify({"success": True, "message": "valid token"})


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error("Server Error: %s", error)
    return jsonify({"success": False, "error": 500, "message": "Internal Server Error"}), 500


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=7003, allow_unsafe_werkzeug=True)
