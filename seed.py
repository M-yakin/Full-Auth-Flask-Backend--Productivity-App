"""Seed database with dropshipping items and demo user."""
from config import app, db
from models import User, Product, Order

with app.app_context():
    print("Clearing old data...")
    Order.query.delete()
    Product.query.delete()
    User.query.delete()

    print("Creating demo user...")
    user = User(username="yakin", email="yakin@example.com", password_hash="password123")
    db.session.add(user)

    print("Creating products...")
    p1 = Product(
        name="AuraGlow LED Wand",
        brand="Lumiere Labs",
        description="Red light therapy skincare wand.",
        price=79.99,
        image_url="https://via.placeholder.com/150"
    )
    p2 = Product(
        name="ZenPulse Massage Gun",
        brand="ZenPulse",
        description="Deep tissue percussion massager.",
        price=119.99,
        image_url="https://via.placeholder.com/150"
    )
    db.session.add_all([p1, p2])
    db.session.commit()

    print("Database seeded successfully!")
    print("Log in with username: yakin, password: password123")
