from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired



class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __reps__(self):
        return self.product_name, self.qty


class LocationForm(FlaskForm):
    location_name = StringField("Location Name", validators=[DataRequired()])
    submit = SubmitField('Save')

    def __reps__(self):
        return self.location_name

class ProductMovement(FlaskForm):
    product = StringField('Product', validators=[DataRequired()])
    from_location = StringField('From')
    to_location = StringField('To')
    available_qty = IntegerField('Available Qty', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __reps__(self):
        return self.product

