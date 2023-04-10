from flask import Flask, render_template, url_for, redirect, request
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app) # an encryption lib


@app.route('/')
def hello():
  
  return render_template("landingPage.html")

# the sign in page
@app.route("/signin")
def signIn():
  return render_template("signIn.html")
                        
# the sign up page
@app.route("/signup")
def signUp():
  return render_template("signUp.html")

# Add Credenttials to Database and redirect to profile page
@app.route("/signUpValidation", methods=["POST"])
def signupValidation():
  
  # getting the form values
  username = request.form.get('name')
  mail = request.form.get('email')
  password = request.form.get('password')
  
  # encrypt passwords using bcrypt flask-bcrypt, require python3 to work
  pw_hash = bcrypt.generate_password_hash(password)
  
  con = sqlite3.connect('accounts')
  con.row_factory = sqlite3.Row
  
  cur = con.cursor()
  cmd = 'INSERT INTO users (username, mail, password) VALUES("{0}", "{1}", "{2}")'.format( username, mail, pw_hash)
  cur.execute(cmd)
  
  con.commit()
  con.close()

  # TODO: after creating the session redirect to the profile page
  return redirect(url_for("profilePage"))


# Validate Credentials from Database for Login
@app.route("/signInValidation", methods=["POST"])
def signinValidation():
  pass

  # after creating the session redirect to the profile page
  return redirect(url_for("profilePage"))

# Profile Page
@app.route("/profile", methods=["GET"])
def profilePage():
  return render_template("profile.html")

if __name__ == "__main__":
  app.run()
     
  