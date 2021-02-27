from base import *

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://hyper-neutrino:{input('Password >>> ')}@localhost:5432/neutrino"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Helper():
  @classmethod
  def add(cls, **k):
    item = cls(**k)
    db.session.add(item)
    if k.get("__no_commit") != True: db.session.commit()
    return item

  @classmethod
  def remove(cls, obj, __no_commit = False):
    db.session.delete(obj)
    if not __no_commit: db.session.commit() 

class site_issues(db.Model, Helper):
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(255))
  url = db.Column(db.String(255), nullable = False)
  issue = db.Column(db.String(4095), nullable = False)

class users(db.Model, Helper):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255), unique = True, nullable = False)
  email = db.Column(db.String(255), unique = True, nullable = False)
  password = db.Column(db.LargeBinary(128), nullable = False)
  salt = db.Column(db.LargeBinary(16), nullable = False)

db.create_all()

commit = db.session.commit

