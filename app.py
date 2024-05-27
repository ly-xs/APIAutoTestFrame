import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:123456@localhost/guest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 发布会模型
class Event(db.Model):
    __tablename__ = 'sign_event'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    limit = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    address = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)


# 嘉宾模型
class Guest(db.Model):
    __tablename__ = 'sign_guest'
    id = Column(Integer, primary_key=True)
    realname = Column(String(50), nullable=False)
    phone = Column(String(16), unique=True, nullable=False)
    email = Column(String(50), nullable=False)
    sign = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey('sign_event.id'), nullable=False)


def custom_jsonify(data):
    # Serialize the data to JSON
    json_data = json.dumps(data, ensure_ascii=False)
    # Create a Response object with the JSON data
    response = Response(json_data, content_type='application/json; charset=utf-8')
    return response


# 初始化数据库
with app.app_context():
    db.create_all()


@app.route('/api/get_event_list/', methods=['GET'])
def get_event_list():
    eid = request.args.get('eid')
    name = request.args.get('name')

    if not eid and not name:
        return custom_jsonify({"status": 10021, "message": "parameter error"}), 400

    if eid:
        event = Event.query.filter_by(id=eid).first()
        if event:
            return custom_jsonify({
                "status": 200,
                "message": "success",
                "data": {
                    "id": event.id,
                    "name": event.name,
                    "limit": event.limit,
                    "status": event.status,
                    "address": event.address,
                    "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }), 200
        else:
            return custom_jsonify({"status": 10022, "message": "query result is empty"}), 404

    if name:
        event = Event.query.filter(Event.name.like(f"%{name}%")).first()
        if event:
            return custom_jsonify({
                "status": 200,
                "message": "success",
                "data": {
                    "id": event.id,
                    "name": event.name,
                    "limit": event.limit,
                    "status": event.status,
                    "address": event.address,
                    "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }), 200
        else:
            return custom_jsonify({"status": 10022, "message": "query result is empty"}), 404

    return custom_jsonify({"status": 10021, "message": "parameter error"}), 400


@app.route('/api/add_event/', methods=['POST'])
def add_event():
    data = request.form
    eid = data.get('eid')
    name = data.get('name')
    limit = data.get('limit')
    address = data.get('address')
    start_time = data.get('start_time')

    if not all([eid, name, limit, address, start_time]):
        return custom_jsonify({"status": 10021, "message": "parameter error"}), 400

    if not eid.isdigit():
        return custom_jsonify({"status": 10021, "message": "parameter error"}), 400

    eid = int(eid)
    limit = int(limit) if limit.isdigit() else None

    if Event.query.filter_by(id=eid).first():
        return custom_jsonify({"status": 10022, "message": "event id already exists"}), 400

    if Event.query.filter_by(name=name).first():
        return custom_jsonify({"status": 10023, "message": "event name already exists"}), 400

    try:
        datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return custom_jsonify({"status": 10024, "message": "start_time format error. "
                                                           "It must be in YYYY-MM-DD HH:MM:SS format."}), 400

    new_event = Event(id=eid, name=name, limit=limit, status=1, address=address, start_time=start_time)
    db.session.add(new_event)
    db.session.commit()
    return custom_jsonify({"status": 200, "message": "add event success", "data": {
        "id": new_event.id,
        "name": new_event.name,
        "limit": new_event.limit,
        "status": new_event.status,
        "address": new_event.address,
        "start_time": new_event.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }}), 201


@app.route('/api/get_guest_list/', methods=['GET'])
def get_guest_list():
    eid = request.args.get('eid')
    phone = request.args.get('phone')

    if not eid:
        return custom_jsonify({"status": 10021, "message": "eid cannot be empty"}), 400

    if not eid.isdigit():
        return custom_jsonify({"status": 10021, "message": "parameter error"}), 400

    eid = int(eid)
    event = Event.query.filter_by(id=eid).first()
    if not event:
        return custom_jsonify({"status": 10022, "message": "query result is empty"}), 404

    if phone:
        guest_list = Guest.query.filter_by(event_id=eid, phone=phone).all()
    else:
        guest_list = Guest.query.filter_by(event_id=eid).all()

    if guest_list:
        return custom_jsonify({
            "status": 200,
            "message": "success",
            "data": [
                {
                    "id": guest.id,
                    "realname": guest.realname,
                    "phone": guest.phone,
                    "email": guest.email,
                    "sign": guest.sign,
                    "event_id": guest.event_id
                } for guest in guest_list
            ]
        }), 200
    else:
        return custom_jsonify({"status": 10022, "message": "query result is empty"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8000)
