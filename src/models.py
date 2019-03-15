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
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable= False)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    qty = db.Column(db.Integer, unique = False, nullable= False)

    def __repr__(self):
        return "Location: "+self.location


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable= False)
    from_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable= False)
    to_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable= False)
    qty = db.Column(db.Integer, unique = False, nullable= False)
