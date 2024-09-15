from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, URLField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional






class signupForm(FlaskForm):
    first_name = StringField("first name", validators=[InputRequired()])
    last_name = StringField("last name", validators=[InputRequired()])
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
class loginForm(FlaskForm):
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
    
class AdminSignupForm(FlaskForm):
    first_name = StringField("first name", validators=[InputRequired()])
    last_name = StringField("last name", validators=[InputRequired()])
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    Admin = StringField("Create a Pin", validators=[InputRequired()])
    
    
class admin_loginForm(FlaskForm):
    Admin_number= StringField("Admin Pin", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
    
class addBook(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    author = StringField("Author", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    