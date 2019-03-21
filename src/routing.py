from flask import render_template, flash, redirect, url_for, request
from src.forms import ProductForm, LocationForm, ProductMovementForm
from src import app
from src.models import db, Product, Location, ProductMovement, LocationProduct
from sqlalchemy import and_


@app.route('/product/<int:product_id>', methods = ['GET', 'POST'])
@app.route('/product', methods = ['GET', 'POST'])
def product(product_id = 0):
    form  = ProductForm()
    method = 'POST'

    if request.method == "POST" and not product_id:
        if form.validate_on_submit():

            prod = Product(product_name = form.product_name.data,  qty= form.qty.data)
            db.session.add(prod)
            db.session.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('product_list'))
    
    elif request.method == 'GET' and product_id > 0:
        product = getProduct(1)
        if product:
            form.product_name.data  = product.product_name
            form.qty.data  = product.qty

    elif request.method == 'POST' and product_id > 0:
        product = getProduct(product_id)

        product.product_name = form.product_name.data
        product.qty= form.qty.data
        db.session.commit()
        flash('Product updated successfully', 'success')

    return render_template('product.html', form = form, method= method)

@app.route('/product-list',methods = ['GET'])
def product_list():
    if request.method == "GET":

        prod_list = Product.query.all()

        if prod_list:
            return render_template('product-list.html', list = prod_list)

    return render_template('product-list.html', list = [])

@app.route('/location/<int:location_id>', methods = ['GET', 'POST'])
@app.route('/location', methods = ['GET', 'POST'])
def location(location_id = 0):
    form  = LocationForm()
    if request.method == "POST" and not location_id:
        if form.validate_on_submit():
            loc = Location(location_name = form.location_name.data)
            db.session.add(loc)
            db.session.commit()
            flash('Loation added successfully', 'success')
            return redirect(url_for('location_list'))

    elif request.method == "GET" and location_id > 0:
        location = getLocation(location_id)
        if location:
            form.location_name.data = location.location_name
            
    elif request.method == 'POST' and location_id > 0:
        location = getLocation(location_id)
        
        location.location_name = form.location_name.data
        db.session.commit()
        
        flash('Loation updated successfully', 'success')

    return render_template('location.html', form = form)
    
@app.route('/location-list',methods = ['GET'])
def location_list():
    if request.method == "GET":
        locations = Location.query.all()
    else:
        locations = []

    return render_template('location-list.html', list  = locations)


@app.route('/product-movement/<int:movement_id>', methods = ['GET', 'POST'])
@app.route('/product-movement', methods = ['GET', 'POST'])
def product_movement(movement_id = 0):
    form  = ProductMovementForm()
    
    products = getProducts()
    locations = getLocations()

    form.product.choices  = [(str(product.id), product.product_name) for product in products]
    form.from_location.choices  = [("0", "---")]+[(str(location.id), location.location_name) for location in locations]
    form.to_location.choices  = [("0", "---")]+[(str(location.id), location.location_name) for location in locations]

    if request.method == "POST" and not movement_id:
        if form.validate_on_submit():
            product_id = form.product.data
            from_location  = form.from_location.data
            to_location = form.to_location.data

            pm = ProductMovement(product_id = product_id,
                                from_location_id = from_location,
                                to_location_id = to_location,
                                qty = form.qty.data)

            # movement_status = move_from_to_location(from_location, to_location, product_id, form.qty.data)

            status =  updateLocationProduct(form)

            if status:
                db.session.add(pm)
                db.session.commit()
                        
                flash('Product moved successfully', 'success')
                return redirect(url_for('product_movement_list'))
            else:
                flash('Failed to moved product', 'danger')
    elif request.method == 'GET' and movement_id > 0:

        product_movement = getProductMovement(movement_id)

        if product_movement:
            form.product.default = product_movement.product_id
            form.from_location.default = product_movement.from_location_id
            form.to_location.default = product_movement.to_location_id
            form.process()
            form.qty.data = product_movement.qty
            
    
    elif request.method == 'POST' and movement_id > 0:
        product_movement = getProductMovement(movement_id)

        product_movement.from_location_id = form.from_location.data
        product_movement.to_location_id = form.to_location.data
        product_movement.qty = form.qty.data

        # status =  move_from_to_location(int(product_movement.from_location_id), int(product_movement.to_location_id), int(product_movement.product_id), int(form.qty.data)) 
        status =  updateLocationProduct(form)

        if status:
            db.session.commit()
            flash('Product movement updated successfully', 'success')
            return redirect(url_for('product_movement_list'))
        else:
            flash('Failed to update product movement', 'danger')
    
    return render_template('move_product.html', form = form)

@app.route('/product-movement-list',methods = ['GET'])
def product_movement_list():
    pm_list = ProductMovement.query.all()
    if pm_list:
        return render_template('product-movement-list.html', list = pm_list)
    else:
        return render_template('product-movement-list.html', list = [])

@app.route('/location-products',methods = ['GET'])
def location_product():
    try:
        if request.method == 'GET':
            product_list = LocationProduct.query.all()
        else:
            product_list = []

        return render_template('location-product-list.html', list = product_list)

    except Exception:
        print(Exception)
        print("Exception occured")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


def updateLocationProduct(form):
    # try:
    product_id = form.product.data
    product = Product.query.get(product_id)

    if int(form.from_location.data) > 0 and int(form.to_location.data) > 0:
        from_product = getLocationProduct(int(form.from_location.data), product_id)
        to_product = getLocationProduct(int(form.to_location.data), product_id)

        if from_product and to_product:
            from_product.qty -= form.qty.data
            to_product.qty += form.qty.data
            db.session.commit()
        else:
            from_loc = LocationProduct(location_id = form.from_location.data,
                                        product_id = form.product.data, 
                                        qty = form.qty.data)

            to_loc = LocationProduct(location_id = form.to_location.data,
                                        product_id = form.product.data, 
                                        qty = form.qty.data)
            db.session.add([from_loc, to_loc])
            db.session.commit()
        

    elif int(form.from_location.data) > 0 and int(form.to_location.data) <= 0:
        
        location = LocationProduct.query.filter(
                LocationProduct.location_id == form.from_location.data, LocationProduct.product_id == form.product.data
            ).first()

        if location:
            location.qty -= form.qty.data
            db.session.commit()
        else:
            location = LocationProduct(location_id = form.from_location.data,
                                        product_id = form.product.data, 
                                        qty = form.qty.data)

            
        product = getProduct(form.product.data)
        if product:
            product.qty += form.qty.data
            db.session.add(location)
            db.session.commit()

    elif int(form.to_location.data) > 0 and int(form.from_location.data) <= 0:
        location = LocationProduct.query.filter(
                LocationProduct.location_id == form.to_location.data, LocationProduct.product_id == form.product.data
            ).first()

        if location:
            location.qty += form.qty.data
            db.session.commit()
        else:
            location = LocationProduct(location_id = form.to_location.data,
                                        product_id = form.product.data, 
                                        qty = form.qty.data)
            db.session.add(location)

        product = getProduct(form.product.data)
        
        if product:
            product.qty -= form.qty.data
            db.session.commit()
    
    return True
    # except Exception as e:
    #     print(str(e))
    #     return False

def move_from_to_location(from_location = 0, to_location = 0, product_id = 0, qty = 0):
    if int(from_location) > 0 and int(to_location) > 0:
        from_product = getLocationProduct(from_location, product_id)

        to_product = getLocationProduct(from_location, product_id)

        if from_product and to_product:
            if from_product.qty >= to_product.qty:  
                from_product.qty -= qty
                to_product.qty += qty
            else:
                flash("Required quantity not available", 'danger')
                return False
        else:
            return False

    elif int(from_location) <= 0 and int(to_location) > 0:
        to_product = getLocationProduct(from_location, product_id)

        if to_product:
            product = getProduct(product_id)
            if product.qty > to_product.qty: 
                to_product.qty += qty
            else:
                flash('Required quantity not available', 'danger')
                return False
        else:
            return False

    elif int(from_location) > 0 and int(to_location) <= 0:
        from_product = getLocationProduct(from_location, product_id)

        if from_product:
            if from_product.qty >= qty:
                from_product.qty -= qty
            else:
                flash('Required quantity not available', 'danger')
                return False
        else:
            return False

    db.session.commit()
    return True

def getProduct(product_id):
    if product_id:
        product = Product.query.get(product_id)

        if product:
            return product
        else:
            return None

def getLocation(location_id):
    if location_id:
        location = Location.query.get(location_id)
        if location:
            return location
        else:
            return None

def getLocationProduct(location_d = 0, product_id = 0):
    if location_d > 0:
        product = LocationProduct.query.filter(LocationProduct.location_id == location_d,
                                                LocationProduct.product_id == product_id).first()
        if product: 
            return product 
        else: 
            return None
    else:
        return None

def getProductMovement(movement_id):
    if movement_id > 0:
        movement = ProductMovement.query.get(movement_id)

        if movement:
            return movement
        else:
            return None
    else:
        return None

def getProducts():
    return Product.query.all()

def getLocations():
    return Location.query.all()