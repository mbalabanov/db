from flask import Flask, render_template, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, db

db.create_all()

app = Flask(__name__)

@app.route("/")
def index():
        active = "active"
        email_address = request.cookies.get("email")

        if email_address:
                user = db.query(User).filter_by(email=email_address).first()
                userEmail = user.email
                userName = user.name
        else:
                userName = None
                userEmail = "Not logged in"

        return render_template("index.html", active0 = active, emailAddress = userEmail, user = userName)

@app.route("/", methods=["POST"])
def login():
        active = "active"
        email = request.form["email"]
        password = request.form["pwd"]
        check_em = db.query(User).filter_by(email=email).first()

        if check_em is None:
                successMessage = "The email address or password is wrong!"
                successClass = "alert alert-danger"
                user = None

                return render_template("index.html", active0=active, successMessage = successMessage, successClass = successClass, user=user)

        elif check_em.check_password(password):
                successMessage = "You have successfully logged on!"
                successClass = "alert alert-success"
                name=check_em.name
                response = make_response(
                        render_template("index.html", successMessage=successMessage, successClass=successClass, emailAddress=email, active0=active, user=name))
                response.set_cookie("email", email)

                return response
        else:
                successMessage = "The email address or password is wrong!"
                successClass = "alert alert-danger"
                user = None
                return render_template("index.html", active0=active, successMessage = successMessage, successClass = successClass, user=user)

@app.route("/form", methods=["GET"])
def form():
        active = "active"
        email_address = request.cookies.get("email")

        if email_address:
                user = db.query(User).filter_by(email=email_address).first()
                userEmail = user.email
        else:
                userEmail = "Not logged in"

        return render_template("form.html", active1 = active, emailAddress = userEmail)

@app.route("/form", methods=["POST"])
def success():
        active = "active"
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pwd"]
        password_hash = generate_password_hash(password)
        name_exists = db.query(User).filter_by(name=name).first()
        email_exists = db.query(User).filter_by(email=email).first()

        if name_exists or email_exists:
                successMessage = "The username or email address already exists!"
                successClass = "alert alert-danger"
                return render_template("form.html", active1=active, successMessage = successMessage, successClass = successClass)
        else:
                user_registration = User(name=name, email=email, password_hash=password_hash)
                successMessage = "You have successfully registered!"
                successClass = "alert alert-success"

                db.add(user_registration)
                db.commit()

                response = make_response(render_template("index.html", successMessage=successMessage, successClass=successClass, emailAddress=email, active0=active, user=name))
                response.set_cookie("email", email)

                return response

@app.route("/admin")
def admin():
        active = "active"
        all_users = db.query(User).all()
        email_address = request.cookies.get("email")

        if email_address:
                user = db.query(User).filter_by(email=email_address).first()
                userEmail = user.email
        else:
                userEmail = "Not logged in"

        return render_template("admin.html", users=all_users, active3=active, emailAddress=userEmail)

if __name__== "__main__":
    app.run(debug=True)
