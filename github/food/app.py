from flask import Flask, request, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodiehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category = db.Column(db.String(50))
    image = db.Column(db.String(200))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total = db.Column(db.Integer)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    item = db.Column(db.String(100))
    price = db.Column(db.Integer)

# ================= ROUTES =================

@app.route("/menu")
def get_menu():
    items = Menu.query.all()
    return jsonify([
        {
            "id": i.id,
            "name": i.name,
            "price": i.price,
            "category": i.category,
            "image": i.image
        }
        for i in items
    ])

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed = generate_password_hash(data["password"])

    db.session.add(User(
        username=data["username"],
        password=hashed
    ))
    db.session.commit()
    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"user_id": user.id})

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/order", methods=["POST"])
def order():
    data = request.json

    new_order = Order(
        user_id=data["user_id"],
        total=data["total"]
    )
    db.session.add(new_order)
    db.session.commit()

    for item in data["items"]:
        db.session.add(OrderItem(
            order_id=new_order.id,
            item=item["name"],
            price=item["price"]
        ))

    db.session.commit()
    return jsonify({"message": "Order placed", "order_id": new_order.id})
    
@app.route("/")
def home():
    return render_template("index.html")


# ================= START =================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)