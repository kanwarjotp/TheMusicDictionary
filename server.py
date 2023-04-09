from flask import Flask, render_template


app = Flask(__name__)


# TODO: create the controller and views for the landing page
@app.route('/')
def hello():
  
  return render_template("landingPage.html")

# TODO: create the above for a login/signup Page
@app.route("/signin")
def sign_in():
  return render_template("sign_in.html")
 
# TODO: create a database to store login credentials

if __name__ == "__main__":
  app.run()
    