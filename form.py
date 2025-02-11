from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length,  Regexp






class signupForm(FlaskForm):
    first_name = StringField("first name", validators=[InputRequired(),  Length(min=3, max=50),
        Regexp('^[A-Za-z]*$', message="Only alphabetic characters are allowed.")])
    
    last_name = StringField("last name", validators=[InputRequired(), Length(min=3, max=50), 
        Regexp('^[A-Za-z]*$', message="Only alphabetic characters are allowed.")])
    
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
class loginForm(FlaskForm):
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
class AdminSignupForm(FlaskForm):
    first_name = StringField("first name", validators=[InputRequired(),Length(min=3, max=50), 
        Regexp('^[A-Za-z]*$', message="Only alphabetic characters are allowed.")])
    
    last_name = StringField("last name", validators=[InputRequired(), Length(min=3, max=50), 
        Regexp('^[A-Za-z]*$', message="Only alphabetic characters are allowed.")])
    
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    Admin = StringField("Create a Pin", validators=[InputRequired()])
    
    
class admin_loginForm(FlaskForm):
    Admin_number= StringField("Admin Pin", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    
    
    
    
class addBook(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    author = StringField("Author", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    Copies = StringField("copies", validators=[InputRequired()])
    