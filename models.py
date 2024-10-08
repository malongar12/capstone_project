from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    book = db.relationship("Copy", backref="issue", lazy=True)
    admin_num = db.Column(db.Integer, nullable = True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True)
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    copy = db.relationship(
        "Copy", backref=db.backref("posts", lazy=True), cascade="all,delete"
    )
    total_copy = db.Column(db.Integer, default=4)
    issued_copy = db.Column(db.Integer, default=0)
    present_copy = db.Column(db.Integer, default=4)


class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime())
    issued_by = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True, default=None
    )
    date_issued = db.Column(db.DateTime(), default=None)
    date_return = db.Column(db.DateTime(), default=None)
    book = db.Column(db.Integer, db.ForeignKey("book.id"))