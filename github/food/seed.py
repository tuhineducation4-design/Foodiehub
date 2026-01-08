from app import app, db, Menu

with app.app_context():

    # 🚨 CLEAR OLD MENU FIRST
    Menu.query.delete()
    db.session.commit()

    items = [
        Menu(name="Zinger Burger", price=199, category="Burger",
             image="/static/images/zinger.jpg"),

        Menu(name="Chicken Burger", price=179, category="Burger",
             image="/static/images/chicken.jpg"),

        Menu(name="Veg Burger", price=149, category="Burger",
             image="/static/images/veg.jpg"),

        Menu(name="Chicken Bucket (6 pcs)", price=499, category="Bucket",
             image="/static/images/bucket.jpg"),

        Menu(name="French Fries", price=99, category="Sides",
             image="/static/images/Fries.jpg"),

        Menu(name="Pepsi", price=49, category="Drinks",
             image="/static/images/Pepsi.jpg"),
    ]

    db.session.add_all(items)
    db.session.commit()

print("✅ Menu reset & seeded cleanly")
