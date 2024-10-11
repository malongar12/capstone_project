from flask import Flask, render_template, flash, redirect, session
from form import signupForm, loginForm, addBook, AdminSignupForm, admin_loginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Book, db, User, Copy
from models import connect_db
from datetime import datetime, date, timedelta
from secret import SECRET_KEY

bcrypt = Bcrypt()
app = Flask(__name__)

app.app_context().push()


app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:malongar12@localhost:5432/library_db"
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
connect_db(app)


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = signupForm()

    if form.validate_on_submit():
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        password = form.password.data

        if len(password) < 6:
            flash("password need to have 8 or more characters")

        else:

            hashed_password = bcrypt.generate_password_hash(
            password, 12).decode('utf-8')

            user = User(first_name=firstname, last_name=lastname,
                        email=email, password=hashed_password)
            session["user-id"] = user.id
            db.session.add(user)
            db.session.commit()
            return redirect("/")
    return render_template("users/signup.html", form=form)


@app.route("/login",  methods=["GET", "POST"])
def login():
    form = loginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("email or password you enter is incorrect")

        if user:
            compare_password = bcrypt.check_password_hash(
                user.password, password)

            if not compare_password:
                flash("password is incorrect")

            if compare_password:
                session["user-id"] = user.id
                return redirect("/")

    return render_template("users/login.html", form=form)


@app.route("/admin/signup", methods=["GET", "POST"])
def admin_signup():

    form = AdminSignupForm()

    if form.validate_on_submit():

        try:

            if not form.Admin.data.isdigit():
                raise ValueError("Admin ID must be a numeric value")

            firstname = form.first_name.data
            lastname = form.last_name.data
            email = form.email.data
            password = form.password.data
            admin = int(form.Admin.data)

            hashed_password = bcrypt.generate_password_hash(
            password, 12).decode('utf-8')

            admin_user = User(first_name=firstname, last_name=lastname, email=email,
                          password=hashed_password, admin_num=admin)
            db.session.add(admin_user)
            db.session.commit()

            return redirect("/admin/login")

        except ValueError as ve:
            flash(f"Error: {str(ve)}", 'error')

    return render_template("admin/admin_signup.html", form=form)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = admin_loginForm()

    if form.validate_on_submit():

        try:

            if not form.Admin_number.data.isdigit():
                raise ValueError("Admin pin must be a numeric value")

            admin_number = int(form.Admin_number.data)
            password = form.password.data

            admin = User.query.filter_by(admin_num=admin_number).first()
            
            if not admin:
                flash("admin not found")
                
            if admin:
                compare_password = bcrypt.check_password_hash(admin.password, password)
                
                if compare_password:
                    session["name"] = admin.first_name
                    return redirect("/admin/dashboard")
               
                else:
                    flash("passowrd you enter is incorrect")

        except ValueError as ve:
            flash(f"Error: {str(ve)}", 'error')

    return render_template("admin/admin_login.html", form=form)


@app.route("/admin/dashboard")
def admin_dashboard():

    if "name" not in session:
        return redirect("/admin/login")

    books = Book.query.all()

    return render_template("admin/admin_dashboard.html", books=books)


@app.route("/users")
def all_users():

    if "name" not in session:
        return redirect("/admin/login")

    users = User.query.all()

    return render_template("users/all_users.html", users=users)


@app.route('/user/<int:id>/delete', methods=["GET","DELETE"])
def delete_user(id):

    get_user = User.query.filter_by(id=id).first()

    if get_user:

        db.session.delete(get_user)
        db.session.commit()
        
        flash("user was deleted")

        return redirect("/users")


@app.route("/books")
def books():
    books = Book.query.all()
    return render_template("book/books.html", books=books)


@app.route("/book/<int:id>")
def book_detail(id):
    book = Book.query.get(id)
    if not book:
        flash(f"book with the id of {id}")

    return render_template("book/book_details.html", book=book)


@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if "name" not in session:
        return redirect("/admin/login")

    form = addBook()
    
    if form.validate_on_submit():
        
        try:

            if not form.Copies.data.isdigit():
                raise ValueError("copies value must be a number")
            
            book_title = form.title.data
            book_author = form.author.data
            book_description = form.description.data
            book_copies = int(form.Copies.data)
            
            book = Book(name = book_title, author = book_author, description = book_description, total_copy = book_copies,
                        issued_copy=0, present_copy=4)
            db.session.add(book)
            db.session.commit()
            return redirect("/admin/dashboard")
            
            
        except ValueError as ve:
            flash(f"Error: {str(ve)}", 'error')

    return render_template("book/add_book.html", form=form)



@app.route("/book/<int:id>/delete", methods=["GET", "DELETE"])
def delete_book(id):
    book_being_deleted = Book.query.get_or_404(id)
    
    if book_being_deleted:
        db.session.delete(book_being_deleted)
        db.session.commit()
        
        flash("book was deleted")
        return redirect("/admin/dashboard")




@app.route("/book/<int:id>/issue", methods=["GET", "POST"])
def check_out(id):
       book_id = Book.query.get_or_404(id)
       
       
       if "user-id" not in session:
           flash("please login to checkout a book")
           
           return redirect(f"/book/{id}")
       


       if book_id:
           copy = Copy(issued_by=session.get("user-id"), date_issued=datetime.now(),
                   date_return=datetime.now() + timedelta(days=1), book=book_id.id)

           book_id.total_copy = -1
           book_id.present_copy = -1
           book_id.issued_copy = +1
           db.session.add(book_id)
           db.session.commit()
       
           db.session.add(copy)
           db.session.commit()
       
       return redirect("/book/issued/view")


@app.route("/book/issued/view")
def issued_book_info():
    
    book_1 = Copy.query.filter_by(issued_by = session.get("user-id")).first()
    
    return render_template("book/issued_book_info.html", book_1 = book_1)




@app.route("/books/issued")
def issue_book():
    
    if "name" not in session:
        return redirect("/")

    
    all_issued_book = Copy.query.all()
    
    return render_template("admin/issued.html", all_issued_book =all_issued_book)



@app.route("/book/<int:book_id>/return", methods= ["GET", "POST"])
def return_book(book_id):
    
  book_id = Copy.query.filter_by(book= book_id).first()
  
  if book_id:
      
      
      db.session.delete(book_id)
      db.session.commit()
  
      
      return redirect("/")
      
  
  
    
@app.route("/admin/logout")
def addmin_logout():
    
    session.pop("name")
    
    return redirect("/")




@app.route("/logout")
def logout():
    session.pop("user-id")
    
    return redirect("/")







if __name__ == '__main__':
    app.run(debug=True)