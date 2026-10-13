from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    payment = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Новая')
    review = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('requests', lazy=True))