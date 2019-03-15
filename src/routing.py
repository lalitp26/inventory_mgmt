from flask import render_template, flash, redirect, url_for
from forms import ProductForm, LocationForm, ProductMovement
from src import app

@app.route('/product', methods = ['GET', 'POST'])
def product():
    form  = ProductForm()
    if form.validate_on_submit():
        flash('Product added successfully', 'success')
        return redirect(url_for('product_list'))

    return render_template('product.html', form = form)

@app.route('/product-list',methods = ['GET'])
def product_list():
    return render_template('product-list.html')

@app.route('/location', methods = ['GET', 'POST'])
def location():
    form  = LocationForm()
    if form.validate_on_submit():
        flash('Loation added successfully', 'success')
        return redirect(url_for('location_list'))
    return render_template('location.html', form = form)
    
@app.route('/location-list',methods = ['GET'])
def location_list():
    return render_template('location-list.html')


@app.route('/product-movement', methods = ['GET', 'POST'])
def product_movement():
    form  = ProductMovement()
    if form.validate_on_submit():
        flash('Product moved successfully', 'success')
        return redirect(url_for('product_movement_list'))
        
    return render_template('move_product.html', form = form)

@app.route('/product-movement-list',methods = ['GET'])
def product_movement_list():
    return render_template('product-movement-list.html')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')