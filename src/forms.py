from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired



class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')


class LocationForm(FlaskForm):
    location_name = StringField("Location Name", validators=[DataRequired()])
    submit = SubmitField('Save')

class ProductMovementForm(FlaskForm):
    product = SelectField('Product', validators=[DataRequired()], id='select_product')
    from_location = SelectField('From', id='select_from_location')
    to_location = SelectField('To', id='select_to_location')
    available_qty = IntegerField('Available Qty', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

