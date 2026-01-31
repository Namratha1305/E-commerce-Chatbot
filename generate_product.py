import os
import sqlite3
import random
from faker import Faker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

print("BASE_DIR:", BASE_DIR)
print("IMAGES_DIR:", IMAGES_DIR)

# Initialize Faker for generating mock data
fake = Faker()

# --- DATABASE SETUP ---
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# --- Products Table ---
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    stock INTEGER NOT NULL,
    image_url TEXT
)
""")
print("Database table 'products' created successfully.")

# --- Chat History Table ---
cursor.execute("DROP TABLE IF EXISTS chat_history")
cursor.execute("""
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
print("Database table 'chat_history' created successfully.")

# --- Users Table (NEW) ---
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
print("Database table 'users' created successfully.")


# --- DATA GENERATION for Products ---
categories = ['Electronics', 'Books', 'Apparel', 'Home & Kitchen', 'Sports & Outdoors']
products_to_add = []
for i in range(105):
    category = random.choice(categories)
    name = ""
    if category == 'Electronics':
        name = f"{random.choice(['Wireless', 'Bluetooth', 'Smart', '4K', 'Portable'])} {random.choice(['Headphones', 'Speaker', 'Watch', 'Monitor', 'Keyboard'])}"
    elif category == 'Books':
        name = fake.catch_phrase().title() + f" by {fake.name()}"
    elif category == 'Apparel':
        name = f"{random.choice(['Cotton', 'Slim-Fit', 'Denim', 'Graphic'])} {random.choice(['T-Shirt', 'Jacket', 'Jeans', 'Hoodie'])}"
    elif category == 'Home & Kitchen':
        name = f"{random.choice(['Stainless Steel', 'Non-Stick', 'Ergonomic', 'Smart'])} {random.choice(['Cookware Set', 'Blender', 'Coffee Maker', 'Air Fryer'])}"
    elif category == 'Sports & Outdoors':
        name = f"{random.choice(['Lightweight', 'Waterproof', 'Insulated', 'Durable'])} {random.choice(['Backpack', 'Tent', 'Running Shoes', 'Water Bottle'])}"

    price = round(random.uniform(15.50, 499.99), 2)
    description = fake.paragraph(nb_sentences=3)
    stock = random.randint(0, 150)
    category_folder_name = category.lower().replace(' & ', '_and_').replace(' ', '_')
    image_files_in_category = os.listdir(f'images/{category_folder_name}')
    chosen_image = random.choice(image_files_in_category)
    image_url = f'images/{category_folder_name}/{chosen_image}'
    products_to_add.append((name, category, price, description, stock, image_url))

cursor.executemany("INSERT INTO products (name, category, price, description, stock, image_url) VALUES (?, ?, ?, ?, ?, ?)", products_to_add)
print(f"{len(products_to_add)} mock products have been added to the database.")

# --- FINALIZE AND CLOSE ---
conn.commit()
conn.close()
print("Database connection closed.")
