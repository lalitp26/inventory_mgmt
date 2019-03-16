from . import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(100), unique = True, nullable= False)
    qty = db.Column(db.Integer, unique = False, nullable= False)

    def __repr__(self):
        return 'Product: '+str(self.product_name)+' qty: '+  str(self.qty)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location_name = db.Column(db.String(100), unique = True, nullable= False)
    products = db.relationship('LocationProduct', backref='products', lazy= True)

    def __repr__(self):
        return 'Location: '+self.location_name

class LocationProduct(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable= False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    qty = db.Column(db.Integer, unique = False, nullable= False)

    product = db.relationship('Product', foreign_keys=[product_id],  backref='location_product_name', lazy= True)
    locaion = db.relationship('Location', foreign_keys=[location_id],  backref='product_location', lazy= True)

    def __repr__(self):
        return ' Location: '+  str(self.location_id)


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    product = db.relationship('Product', backref='product', lazy= True)

    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    from_location = db.relationship('Location', foreign_keys=[from_location_id],  backref='from_location', lazy= True)
    
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location = db.relationship('Location', foreign_keys=[to_location_id],  backref='to_location', lazy= True)
    
    qty = db.Column(db.Integer, unique = False, nullable= False)
    
