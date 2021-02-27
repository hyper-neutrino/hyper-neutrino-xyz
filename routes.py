import re, sys

from auth import *
from base import *
from db import *

from datetime import datetime, timezone

args = sys.argv[1:]

def render(*a, **k):
  return render_template(*a, **k, user = user, __navbar_elements = [("/", "Home"), ("/about", "About"), ("/contact", "Contact"), ("/projects", "Projects")])

@app.route("/")
def serve_root():
  return render("index.html")

@app.route("/about")
def serve_about():
  return render("about.html")

@app.route("/contact")
def serve_contact():
  return render("contact.html")

@app.route("/projects")
def serve_projects():
  return render("projects.html")

@app.route("/signin", methods = ["GET", "POST"])
def serve_signin():
  if request.method == "GET":
    return render("signin.html")
  elif request.method == "POST":
    u = users.query.filter_by(username = request.form["username"]).first()
    
    if u and passhash(request.form["password"], u.salt) == u.password:
      response = make_response(redirect(request.args.get("next", "/"), code = 303))
      response.set_cookie("user", make_jwt({
        "uid": u.id,
        "exp": int(datetime.now(timezone.utc).timestamp()) + 60 * 60 * 24 * 7
      }))

      set_user(u, True)

      return response
    
    flash("Invalid credentials!", "error")
    return render("signin.html", _username = request.form["username"])

@app.route("/signup", methods = ["GET", "POST"])
def serve_signup():
  if request.method == "GET":
    return render("signup.html")
  elif request.method == "POST":
    fail = False
    
    fail = fail or validate_username(request.form["username"])
    fail = fail or validate_email(request.form["email"])
    fail = fail or validate_password(request.form["password"], request.form["repeatpass"])
    
    if fail:
      return render("signup.html", _username = request.form["username"], _email = request.form["email"])
    
    salt = random_salt()
    u = users.add(username = request.form["username"], email = request.form["email"], password = passhash(request.form["password"], salt), salt = salt)
    
    response = make_response(redirect(request.args.get("next", "/"), code = 303))
    response.set_cookie("user", make_jwt({
      "uid": u.id,
      "exp": int(datetime.now(timezone.utc).timestamp()) + 60 * 60 * 24 * 7
    }))
    
    set_user(u, True)
    
    return response

@app.route("/logout")
def serve_logout():
  response = make_response(redirect(request.args.get("next", "/"), code = 303))
  response.set_cookie("user", "")
  return response

@app.route("/edit-profile", methods = ["GET", "POST"])
def serve_edit_profile():
  if user is None:
    return redirect("/login?next=/edit-profile", code = 303)
  if request.method == "GET":
    return render("edit-profile.html")
  elif request.method == "POST":
    fail = False
    
    if request.form["username"] != user.username:
      fail = fail or validate_username(request.form["username"])
    
    if request.form["email"] != user.email:
      fail = fail or validate_email(request.form["email"])
    
    if request.form["oldpass"] or request.form["newpass"]:
      if not request.form["oldpass"]:
        fail = True
        flash("Please enter your old password to change your password!", "error")
      elif passhash(request.form["oldpass"], user.salt) != user.password:
        fail = True
        flash("Incorrect password!", "error")
      
      fail = fail or validate_password(request.form["newpass"], request.form["repeatpass"])
    
    if fail:
      return render("edit-profile.html", _username = request.form["username"], _email = request.form["email"])
    
    user.username = request.form["username"]
    user.email = request.form["email"]
    
    if request.form["newpass"]:
      user.password = passhash(request.form["newpass"], user.salt)
    
    commit()
    
    flash("Updated your user information!", "success")
    return render("edit-profile.html")

@app.route("/tos")
def serve_tos():
  return render("tos.html")

@app.route("/privacy")
def serve_privacy():
  return render("privacy.html")

@app.route("/report-an-issue", methods = ["GET", "POST"])
def serve_report():
  if request.method == "GET":
    return render("report.html")
  elif request.method == "POST":
    site_issues.add(email = request.form["email"], url = request.form["url"], issue = request.form["issue"])
    return redirect("/", code = 303)

@app.errorhandler(404)
def serve_404(e):
  return render("404.html")

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5555, debug = "debug" in args)