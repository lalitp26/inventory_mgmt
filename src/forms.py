from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired



class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')


class LocationForm(FlaskForm):
    location_name = StringField("Location Name", validators=[DataRequired()])
    submit = SubmitField('Save')

class ProductMovement(FlaskForm):
    product = StringField('Product', validators=[DataRequired()])
    from_location = StringField('From')
    to_location = StringField('To')
    available_qty = IntegerField('Available Qty', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

