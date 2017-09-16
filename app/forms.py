from flask_wtf import Form, FlaskForm
from wtforms import validators, ValidationError, TextField, StringField, IntegerField, PasswordField, TextAreaField, SubmitField, RadioField, SelectField, BooleanField
from wtforms.validators import (DataRequired, ValidationError, Email,
                                Length, EqualTo)

class LoginForm(FlaskForm):
   username = TextField("username",[validators.Required()])
   password = PasswordField("password", [validators.Required()])
   submit = SubmitField("submit")
   
class RegistrationForm(FlaskForm):
    username = TextField("username", [validators.Required()])
    email = TextField("email", [validators.Required(), validators.Email()])
    password = PasswordField("password", [validators.Required()])
    
    submit = SubmitField("submit")

class ShoppingListForm(FlaskForm):
    listname = TextField("ListName",[validators.Required()])
    
    submit = SubmitField("submit")
    

class additemsForm(FlaskForm):
    itemname = TextField("itemname",[validators.Required()])
    list_id = StringField('list_id')
    price = IntegerField("price")
    quantity = IntegerField("quantity")
    submit = SubmitField("submit")
