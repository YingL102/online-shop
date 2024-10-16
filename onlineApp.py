from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True, unique = True)
    price = db.Column(db.Integer)
    image = db.Column(db.Text)
    description = db.Column(db.Text)
    environmental_impact_rating = db.Column(db.Integer)

class AddToBasketForm(FlaskForm):
    quantity = IntegerField('Quantity: ', validators = [DataRequired(), NumberRange(min=0,max=100)])
    submit = SubmitField('Add to basket')

@app.route('/', methods = ['GET', 'POST'])
def galleryPage():
    products_query = Product.query.all()
    forms = {product.id: AddToBasketForm(prefix=str(product.id)) for product in products_query}

    if request.method == 'POST':
        for product_id, form in forms.items():
            if form.validate_on_submit():
                if 'products' not in session:
                    session['products'] = []
                product_exists = False
                for product in session['products']:
                    if product[0] == product_id:
                        product[1] += form.quantity.data
                        product_exists = True
                if not product_exists:
                    session['products'].append([product_id, form.quantity.data])
                session.modified = True
                return redirect(url_for('galleryPage'))

    sort_option = request.args.get('sort', 'name')

    if sort_option == 'price':
        products_query = Product.query.order_by(Product.price).all()
    elif sort_option == 'environmental_impact_rating':
        products_query = Product.query.order_by(Product.environmental_impact_rating).all()
    else: 
        products_query = Product.query.order_by(Product.name).all()

    return render_template('index.html', products = products_query, forms = forms)

@app.route('/product/<int:productId>', methods = ['GET','POST'])
def singleProductPage(productId):
    form = AddToBasketForm()
    products_query = Product.query.all()

    if form.validate_on_submit():

        if 'products' not in session:
            print("New session", flush = True)
            session['products'] = []

        product_exists = False
        for product in session['products']:
            if (product[0] == productId):
                if product[1] is not None:
                    product[1] = int(product[1]) + int(form.quantity.data)
                else:
                    product[1] = 0
                product[1] = int(product[1]) + int(form.quantity.data)
                print(product[1])
                session.modified = True
                product_exists = True
                break
        
        if not product_exists:
            session['products'] += [[productId, form.quantity.data]]

        return render_template('singleProductPageQuantity.html', product = products_query[productId - 1], quantity = form.quantity.data, form = form)
    else:
        return render_template('singleProductPage.html', product = products_query[productId - 1], form = form)
    
@app.route('/basket', methods = ['GET', 'POST'])
def basketPage():

    products = []
    quantities = []
    total_price = 0

    if 'products' in session:
        for productId, quantity in session['products']:
            products.append(productId)
            quantities.append(quantity)
        print(quantities)
        print(products)

        products_query = Product.query.filter(Product.id.in_(products)).all()

        for products, quantity in zip(products_query, quantities):
            total_price += products.price * quantity

        session['total_price'] = total_price
        session.modified = True

        return render_template('basketPage.html', products = products_query, quantities = quantities , total_price = total_price)
    else: 
        return render_template('basketPage.html', products = [], quantities = [], total_price = 0)

    
@app.route('/removeItem/<int:index>', methods = ['GET', 'POST'])
def removeItem(index):
    
    if 'products' in session:
        products = session['products']
        if index < len(products):
            del products[index]
            session['products'] = products
            session.modified = True
    
    return redirect(url_for('basketPage'))

@app.route('/checkout', methods = ['GET', 'POST'])
def checkoutPage():
    form = PaymentForm()

    total_price = session.get('total_price', 0)

    if form.validate_on_submit():
        return render_template('checkoutSuccessful.html')
    else:
        return render_template('checkoutPage.html', form = form, total_price = total_price)

@app.route('/checkoutsuccessful')
def checkoutSuccessful():
    return render_template('checkoutSuccessful.html')

def validateCardNumber(form, field):
    cardNumber = field.data.replace(' ', '').replace('-','')

    if not (len(cardNumber) == 16 and cardNumber.isdigit()):
        raise ValidationError('Invalid credit/debit card number') 

def validateExpiryDate(form, field):
    if field.data != 5 and '/' not in field.data:
        raise ValidationError('Invalid expiry date (Please use "/" to separate month and year)')
    
def validateCVV(form, field):
    if field.data and not (len(field.data) == 3 or not field.data.isdigit()):
        raise ValidationError('Invalid CVV')
    
class PaymentForm(FlaskForm):
    cardNumber = StringField('Credit/Debit Card Number: ', validators = [DataRequired(), Length(min = 16, max = 19), validateCardNumber])
    expiryDate = StringField('Expiry Date (MM/YY) ', validators = [DataRequired(), Length(min=5, max = 5), validateExpiryDate])
    cvv = StringField('CVV', validators = [DataRequired(),Length(min = 3, max = 3), validateCVV])
    pay = SubmitField('Click to pay')

if __name__ == '__main__':
    app.run(debug=True)
    