from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import JSON
from .extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255))
    role = db.Column(db.String(50), default="user")

    forests = db.relationship("Forest", backref="owner", lazy=True)
    chats = db.relationship("ChatHistory", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Forest(db.Model):
    __tablename__ = "forests"
    forest_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    location = db.Column(db.String(255))
    area = db.Column(db.Float)
    coordinates = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    data = db.relationship("ForestData", backref="forest", uselist=False)
    analyses = db.relationship("Analysis", backref="forest", lazy=True)


class ForestData(db.Model):
    __tablename__ = "forest_data"
    data_id = db.Column(db.Integer, primary_key=True)
    forest_id = db.Column(db.Integer, db.ForeignKey("forests.forest_id"), nullable=False)
    tree_count = db.Column(db.Integer)
    soil_data = db.Column(JSON)
    animal_data = db.Column(JSON)
    calamity_history = db.Column(JSON)


class Analysis(db.Model):
    __tablename__ = "analysis"
    analysis_id = db.Column(db.Integer, primary_key=True)
    forest_id = db.Column(db.Integer, db.ForeignKey("forests.forest_id"), nullable=False)
    risk_zones = db.Column(JSON)  # GeoJSON or grid-based structure
    recommendations = db.Column(JSON)
    heat_map_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class CaseStudy(db.Model):
    __tablename__ = "case_studies"
    case_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    success_metrics = db.Column(JSON)


class ForumPost(db.Model):
    __tablename__ = "forum"
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
