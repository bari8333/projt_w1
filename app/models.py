from app import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'device_type': self.device_type,
            'status': self.status,
            'location': self.location
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"
