# E-commerce Sales Chatbot

## 1. Project Summary

This project is a comprehensive, interactive e-commerce sales chatbot developed to fulfill the requirements of a technical case study. The application provides a seamless, user-centric shopping experience, allowing users to register, log in, search for products through a conversational interface, manage a shopping cart, and complete a mock checkout process.

The architecture is a modern, decoupled system with a vanilla JavaScript frontend and a Python/Flask backend, ensuring modularity and scalability. The final application goes beyond the basic requirements to include innovative features like smart search suggestions and an interactive, visually-driven UI to enhance the user experience.

---

## 2. How to Access and Interact with the Chatbot

This guide provides a step-by-step walkthrough on how to use the application from a user's perspective.

### Accessing the Application

1.  **Ensure the Server is Running:** Before you begin, the backend server must be active. This is done by running `python app.py` in the terminal from the project folder.
2.  **Open the Login Page:** Open the `login.html` file in your web browser.

### A Sample User Journey

Follow these steps for a complete tour of the chatbot's features:

**Step 1: Register a New Account**
* On the login page, enter any username and password you wish.
* Click the **"Register"** button. You should see a "Registration successful!" message.

**Step 2: Log In**
* Using the same credentials you just registered, click the **"Login"** button.
* You will be successfully logged in and redirected to the main chatbot interface.

**Step 3: Discover Features**
* The chatbot will greet you. To see what's possible, type:
    > `help`

**Step 4: Browse Products Visually**
* To see the product categories, type:
    > `show categories`
* The bot will display interactive buttons. Click a button like **"Electronics"** to see all products in that category, complete with images.

**Step 5: Search for a Product**
* To find a specific item, type a search query like:
    > `search for a watch`
* The chatbot will display relevant products. Notice the "Smart Search" feature may suggest categories if your search term is too broad.

**Step 6: Manage Your Shopping Cart**
* After finding a product you like (e.g., one with ID 96), add it to your cart by typing:
    > `add to cart 96`
* To see the contents of your cart at any time, type:
    > `view cart`
* The cart will show all items, quantities, the total price, and a button to remove items.

**Step 7: Checkout**
* When you are ready to purchase, simply type:
    > `checkout`
* The chatbot will confirm your mock order.

**Step 8: End Your Session**
* To log out securely, type:
    > `logout`
* You will be redirected back to the login page.

---

## 3. Key Features

* **Secure User Authentication**: Full registration and login system using password hashing (`bcrypt`) and token-based sessions (`Flask-JWT-Extended`).
* **Conversational Product Search**: Users can search for products using natural language.
* **Smart Search Suggestions**: If a search yields no results but matches a category, the chatbot intelligently suggests products from that category.
* **Interactive & Visual UI**: Products are visualized with images, and categories are presented as one-click filter buttons.
* **Persistent Shopping Cart**: The cart state is saved in the browser's `localStorage`, allowing the user's session to survive page reloads.
* **Full Database Integration**: All product, user, and chat history data is stored in and retrieved from a relational SQLite database.
* **Fault-Tolerant Checkout**: The system validates product stock in real-time before processing an order.

---

## 4. Technology Stack & Rationale

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend** | Python, Flask | Flask was chosen for its lightweight, micro-framework nature, making it perfect for building a focused RESTful API without unnecessary bloat. |
| **Frontend**| Vanilla JavaScript, HTML5, CSS3 | By avoiding a large framework, this project showcases strong foundational web development skills and keeps the application fast with zero frontend dependencies. |
| **Database** | SQLite | A serverless, file-based RDBMS ideal for self-contained projects, providing full SQL capabilities without the overhead of a separate database server. |
| **Security** | Flask-Bcrypt, Flask-JWT-Extended | This combination provides an industry-standard security model. `bcrypt` ensures passwords are never stored in plaintext, while JWTs offer a stateless, secure method for authenticating API requests. |
| **Data Generation**| Faker | Used to programmatically create a realistic and richly populated mock database, enabling robust testing and demonstration. |

---

## 5. Local Setup for Developers

Follow these steps to run the application locally on your machine.

#### Prerequisites
- Python 3.8+
- `pip` package manager
- Git

#### Installation
1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install the required packages from `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Generate the database and mock data:**
    ```bash
    python generate_product.py
    ```
5.  **Run the backend server:**
    ```bash
    python app.py
    ```
6.  **Launch the application:** Open `login.html` in your web browser.

---

## 6. API Endpoints

All endpoints except `/register` and `/login` require a valid JWT `access_token` in the `Authorization: Bearer <token>` header.

| Method | Endpoint | Protection | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/register`| Public | Registers a new user with a hashed password. |
| `POST` | `/login` | Public | Logs in a user and returns a JWT access token. |
| `GET` | `/products`| JWT Required | Fetches products. Can be filtered with `?query=` or `?category=`. |
| `GET` | `/products/<id>`| JWT Required | Fetches details for a single product by its ID. |
| `POST`| `/checkout`| JWT Required | Processes a mock checkout. Validates stock levels. |
| `POST`| `/chat` | JWT Required | Saves a user or bot chat message to the database history. |
