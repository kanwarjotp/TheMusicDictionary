from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
  
  return render_template("landingPage.html")

# the sign in page
@app.route("/signin")
def signIn():
  return render_template("signIn.html")

# the sign up page
@app.route("/signup")
def sign_Up():
  return render_template("sign_Up.html")
# TODO: create a database to store login credentials

if __name__ == "__main__":
  app.run()
     