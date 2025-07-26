# Wyelle Sports Goods

A simple Flask-based web application for a sports goods online shop. Users can view products, add items to a basket, and complete a checkout process.

## Features

- **Product Gallery:** Browse products with sorting options (by name, price, or environmental impact rating).
- **Product Detail:** View detailed information about each product and add a specified quantity to your basket.
- **Basket Management:** View and modify items in your basket.
- **Checkout:** A basic checkout form with payment validation using Flask-WTF.

## Project Structure

- **[onlineApp.py](onlineApp.py):** Main Flask application including routes, models, and view functions.
- **[StoreItems.py](StoreItems.py):** Script that initializes the database with product data.
- **templates/**  
  Contains all HTML template files:
  - `base.html`
  - `index.html`
  - `singleProductPage.html`
  - `singleProductPageQuantity.html`
  - `basketPage.html`
  - `checkoutPage.html`
  - `checkoutSuccessful.html`
- **static/**  
  Contains CSS and image assets.
- **instance/data.sqlite3:** SQLite database file.

## Requirements

- Python 3.6+
- Flask
- Flask-WTF
- Flask-Bootstrap
- SQLAlchemy

## Installation

1. **Clone the repository or copy the project files** to your local machine.
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```
3. **Install the required packages**:
   ```sh
   pip install flask flask-wtf flask-bootstrap flask-sqlalchemy
   ```

## Running the Application

1. Populate the database by running the [StoreItems.py](StoreItems.py) script:
   ```sh
   python StoreItems.py
   ```
2. Start the Flask development server:
   ```sh
   python onlineApp.py
   ```
3. Open your browser and go to `http://localhost:5000` to view the application.

## Usage

- **Home Page:** Displays a gallery of products. You can sort the products using the provided dropdown.
- **Product Detail:** Click on a product to view more details and add a quantity to your basket.
- **Basket:** View items added to your basket and remove items if needed.
- **Checkout:** Fill out the payment form to complete your order.

## License

This project is for educational purposes.
