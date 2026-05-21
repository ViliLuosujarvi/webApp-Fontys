# ----------------------------------------------------------------
# This file is still in progress and it's purpose is to serve
# as mock connection between the database and the web application 
# ----------------------------------------------------------------


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL connection (CHANGE these values)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:@192.168.189.139/Database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------
# DATABASE MODEL
# -----------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)


# -----------------------
# EXISTING ENDPOINTS (UNCHANGED)
# -----------------------
@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, REST API!"})


@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({
        "you_sent": data
    })


# -----------------------
# NEW TEST ENDPOINTS
# -----------------------

# Create a user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json

    user = User(
        email=data["email"],
        name=data["name"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created"})


# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": u.id,
            "email": u.email,
            "name": u.name
        }
        for u in users
    ])


# -----------------------
# RUN SERVER (UNCHANGED)
# -----------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
