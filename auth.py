from base import *
from db import *

import re

from werkzeug.local import Local

user_mgr = Local()
user = user_mgr("user")

def set_user(obj, update = True):
  user_mgr.user = obj
  user_mgr._update = getattr(user_mgr, "update", False) or update

@app.before_request
def resolve_user():
  if request.endpoint == "static":
    return
  
  set_user(None, False)
  
  try:
    cookie = request.cookies.get("user", "")
    
    if cookie:
      token = verify_jwt(cookie)
      
      if "uid" not in token:
        return
      
      u = users.query.filter_by(id = token["uid"]).first()
      
      if u:
        set_user(u, False)
  except (InvalidJWT, ExpiredJWT):
    pass

def validate_username(string):
  if not string:
    flash("Username must not be empty!", "error")
    return True
  elif not re.match("^(\w|-|_)+$", string):
    flash("Username must only contain alphanumeric characters, dashes, and underscores!", "error")
    return True
  elif users.query.filter_by(username = string).count() > 0:
    flash("This username is already in use!", "error")
    return True
  return False

def validate_email(string):
  if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form["email"]):
    flash("Please enter a valid email address!", "error")
    return True
  elif users.query.filter_by(email = request.form["email"]).count() > 0:
    flash("This email address is already in use!", "error")
    return True
  return False

def validate_password(password, repeatpass):
  fail = False
  
  if len(password) < 8:
    fail = True
    flash("Password must be at least 8 characters long!", "error")

  if password != repeatpass:
    fail = True
    flash("Passwords don't match!", "error")
  
  return fail