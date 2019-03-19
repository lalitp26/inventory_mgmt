from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from src.models import Product, Location


class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_product_name(self, product_name):
        product = Product.query.filter_by(product_name = product_name.data).first()
        
        if product:
            raise ValidationError('Product is already present')


class LocationForm(FlaskForm):
    location_name = StringField("Location Name", validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_location_name(self, location_name):
        location = Location.query.filter_by(location_name = location_name.data).first()
        
        if location:
            raise ValidationError('Location is already present')

class ProductMovementForm(FlaskForm):
    product = SelectField('Product', validators=[DataRequired()], id='select_product')
    from_location = SelectField('From', id='select_from_location')
    to_location = SelectField('To', id='select_to_location')
    available_qty = IntegerField('Available Qty', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

