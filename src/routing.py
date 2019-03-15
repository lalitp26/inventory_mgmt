from flask import render_template, flash, redirect, url_for, request
from forms import ProductForm, LocationForm, ProductMovementForm
from src import app
from src.models import db, Product, Location, ProductMovement

@app.route('/product', methods = ['GET', 'POST'])
def product():
    form  = ProductForm()
    if request.method == "POST":
        if form.validate_on_submit():

            prod = Product(product_name = form.product_name.data,  qty= form.qty.data)
            db.session.add(prod)
            db.session.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('product_list'))
    else:
        return render_template('product.html', form = form)

@app.route('/product-list',methods = ['GET'])
def product_list():
    if request.method == "GET":

        prod_list = Product.query.all()

        if prod_list:
            return render_template('product-list.html', list = prod_list)
        else:
            return render_template('product-list.html', list = [])

@app.route('/location', methods = ['GET', 'POST'])
def location():
    form  = LocationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            loc = Location(location_name = form.location_name.data)
            db.session.add(loc)
            db.session.commit()
            flash('Loation added successfully', 'success')
            return redirect(url_for('location_list'))
    return render_template('location.html', form = form)
    
@app.route('/location-list',methods = ['GET'])
def location_list():
    if request.method == "GET":
        locations = Location.query.all()
    else:
        locations = []

    return render_template('location-list.html', list  = locations)


@app.route('/product-movement', methods = ['GET', 'POST'])
def product_movement():
    form  = ProductMovementForm()
    
    products = getProducts()
    locations = getLocations()

    form.product.choices  = [(str(product.id), product.product_name) for product in products]
    form.from_location.choices  = [(str(location.id), location.location_name) for location in locations]
    form.to_location.choices  = [(str(location.id), location.location_name) for location in locations]

    if request.method == "POST":
        if form.validate_on_submit():
            
            pm = ProductMovement(product = form.product.data,
                                from_location = form.product.data,
                                to_location = form.product.data,
                                qty = form.product.data)

            db.session.add(pm)
            db.session.commit()
            
            flash('Product moved successfully', 'success')
            return redirect(url_for('product_movement_list'))
        else:
            return render_template('move_product.html', form = form)
    else:
        return render_template('move_product.html', form = form)

@app.route('/product-movement-list',methods = ['GET'])
def product_movement_list():
    pm_list = ProductMovement.query.all()
    if pm_list:
        return render_template('product-movement-list.html', list = pm_list)
    else:
        return render_template('product-movement-list.html', list = [])


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


def getProduct(product_id):
    if product_id:
        product = Product.query.get(product_id)

        if product:
            return product
        else:
            return None

def getProducts():
    return Product.query.all()

def getLocations():
    return Location.query.all()