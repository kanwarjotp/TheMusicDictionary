from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
  
  return render_template("landingPage.html")

# the sign in page
@app.route("/signin")
def sign_in():
  return render_template("sign_in.html")

# the sign up page
@app.route("/signup")
def sign_up():
  return render_template("sign_up.html")

# TODO: create a database to store login credentials

if __name__ == "__main__":
  app.run()
    