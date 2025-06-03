from flask import request, jsonify
from app import app, db
from app.models import Device, User
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/devices', methods=['POST'])
@jwt_required()
def add_device():
    data = request.get_json()
    new_device = Device(
        name=data['name'],
        device_type=data['device_type'],
        status=data['status'],
        location=data['location']
    )
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message': 'Device added successfully'}), 201

@app.route('/devices', methods=['GET'])
def get_device():
    device_id = request.args.get('id')
    location = request.args.get('location')

    if device_id:
        device = Device.query.get(device_id)
        if device:
            return jsonify(device.to_dict()), 200
        return jsonify({'message': 'Device not found'}), 404

    elif location:
        device = Device.query.filter_by(location=location).first()
        if device:
            return jsonify(device.to_dict()), 200
        return jsonify({'message': 'Device not found'}), 404

    else:
        devices = Device.query.all()
        return jsonify([device.to_dict() for device in devices]), 200

@app.route('/devices/<int:device_id>', methods=['PUT'])
@jwt_required()
def update_device(device_id):
    data = request.get_json()
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'message': 'Device not found'}), 404

    device.name = data.get('name', device.name)
    device.device_type = data.get('device_type', device.device_type)
    device.status = data.get('status', device.status)
    device.location = data.get('location', device.location)
    db.session.commit()
    return jsonify({'message': 'Device updated successfully'}), 200

@app.route('/devices/<int:device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return jsonify({'message': 'Device not found'}), 404

    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted successfully'}), 200

@app.route('/devices/all', methods=['GET'])
def get_all_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices]), 200