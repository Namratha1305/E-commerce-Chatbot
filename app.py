# app.py

import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)
CORS(app)

# --- Configuration ---
app.config["JWT_SECRET_KEY"] = "your-super-secret-key-change-this" # Change this!
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# --- Database Helper ---
def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Authentication Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user:
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"error": "Invalid credentials"}), 401

# --- Protected Endpoints ---
# All previous endpoints now require a valid JWT token.

# In app.py, replace the get_products function
@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    query = request.args.get('query')
    category = request.args.get('category')
    conn = get_db_connection()
    products = []

    if category:
        products = conn.execute("SELECT * FROM products WHERE category LIKE ?", [f'%{category}%']).fetchall()
    elif query:
        # First, try a direct search on name and description
        products = conn.execute("SELECT * FROM products WHERE name LIKE ? OR description LIKE ?", [f'%{query}%', f'%{query}%']).fetchall()

        # If no results, try a "smarter" search
        if not products:
            # Check if the query matches a category name
            possible_cat = conn.execute("SELECT DISTINCT category FROM products WHERE category LIKE ?", [f'%{query}%']).fetchone()
            if possible_cat:
                # Fetch all products from that category instead
                products = conn.execute("SELECT * FROM products WHERE category = ?", [possible_cat['category']]).fetchall()
                # Add a special flag to the response to let the frontend know this was a suggestion
                response_data = [dict(ix) for ix in products]
                return jsonify({"suggestion": True, "category": possible_cat['category'], "products": response_data})

    else: # No query or category, return all
        products = conn.execute("SELECT * FROM products").fetchall()

    conn.close()
    return jsonify([dict(ix) for ix in products])


@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    # ... (The rest of this function is the same as before) ...
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if product is None: return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product))


@app.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    # ... (The rest of this function is the same as before) ...
    data = request.json
    if not data or "items" not in data: return jsonify({"error": "No items in cart"}), 400
    conn = get_db_connection()
    total = 0
    for item in data["items"]:
        product = conn.execute('SELECT * FROM products WHERE id = ?', (item["product_id"],)).fetchone()
        if product is None: return jsonify({"error": f"Product with ID {item['product_id']} not found."}), 404
        if product['stock'] < item['quantity']: return jsonify({"error": f"Not enough stock for {product['name']}. Only {product['stock']} left."}), 400
        total += product["price"] * item["quantity"]
    conn.close()
    return jsonify({"order_id": 1001, "total": total, "message": "Thank you for your order!"})

@app.route('/chat', methods=['POST'])
@jwt_required()
def save_chat_message():
    # ... (The rest of this function is the same as before) ...
    current_user = get_jwt_identity() # You can optionally associate chats with users
    data = request.json
    sender = data.get('sender')
    message = data.get('message')
    if not sender or not message: return jsonify({"error": "Sender and message are required"}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO chat_history (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Chat history saved."}), 201
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
