from flask import Flask, render_template, flash, redirect, session, request, url_for
from form import signupForm, loginForm, addBook, AdminSignupForm, admin_loginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Book, db, User, Copy
from models import connect_db
from datetime import datetime, date, timedelta
from secret import SECRET_KEY

bcrypt = Bcrypt()
app = Flask(__name__)

# app.app_context().push()
# db.create_all()

app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:malongar12@localhost:5432/library_db"
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
connect_db(app)

with app.app_context():
    db.create_all()


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

        validUser = User.query.filter_by(email=email).first()

        if validUser:

                flash("email already taken")
                return redirect("/signup")

        elif  " " in password or " " in firstname or " " in lastname or " " in email:
                flash("Password, firstname, lastname, and email cannot contain any spaces")
                return redirect("/signup")

        elif len(password) < 4:
                flash("password need to have 4 or more characters")
                return redirect("/signup")
        else:

            hashed_password = bcrypt.generate_password_hash(
            password, 12).decode('utf-8')

            user = User(first_name=firstname, last_name=lastname,
                        email=email, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash("account created successfully")
            return redirect("/login")
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
             return redirect("/login")

        if user:
            compare_password = bcrypt.check_password_hash(
                user.password, password)

            if not compare_password:
                flash("email or password you enter is incorrect")
                return redirect("/login")

            if compare_password:
                session["user-id"] = user.id
                return redirect("/")

    return render_template("users/login.html", form=form)


# admin routes

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
            admin_num = int(form.Admin.data)

            is_Valid_admin = User.query.filter_by(admin_num=admin_num).first()

            if is_Valid_admin:
                flash("Admin pin is associated with another account")
                return redirect("/admin/signup")

            hashed_password = bcrypt.generate_password_hash(
            password, 12).decode('utf-8')

            admin_user = User(first_name=firstname, last_name=lastname, email=email,
                          password=hashed_password, admin_num=admin_num)
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
                return redirect("/admin/login")

            if admin:
                compare_password = bcrypt.check_password_hash(
                    admin.password, password)

                if compare_password:
                    session["admin_num"] = admin.admin_num
                    return redirect("/admin/dashboard")

                else:
                    flash("passowrd you enter is incorrect")
                    return redirect("/admin/login")

        except ValueError as ve:
            flash(f"Error: {str(ve)}", 'error')

    return render_template("admin/admin_login.html", form=form)


@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_num" not in session:
        return redirect("/admin/login")

    per_page = 10
    page = request.args.get('page', 1, type=int)

    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("admin/admin_dashboard.html", books=books)


@app.route("/users")
def all_users():

    if "admin_num" not in session:
        return redirect("/admin/login")

    users = User.query.all()

    return render_template("users/all_users.html", users=users)


@app.route('/user/<int:id>/delete', methods=["GET", "DELETE"])
def delete_user(id):

    get_user = User.query.filter_by(id=id).first()

    if get_user:

        db.session.delete(get_user)
        db.session.commit()

        flash("user was deleted")

        return redirect("/users")


# books routes

@app.route("/books")
def books():
        per_page = 10
        page = request.args.get('page', 1, type=int)

        books = Book.query.paginate(
            page=page, per_page=per_page, error_out=False)

        return render_template("book/books.html", books=books)


@app.route("/book/<int:id>")
def book_detail(id):
    book = Book.query.get(id)
    if not book:
        flash("no book found")
        return redirect("/books")
    
    return render_template("book/book_details.html", book=book)


@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if "admin_num" not in session:
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

            if book_copies <= 0:
                raise ValueError(
                    "The number of copies must be greater than 0.")

            book = Book(name=book_title, author=book_author, description=book_description, total_copy=book_copies,
                        issued_copy=0, present_copy=book_copies)

            db.session.add(book)
            db.session.commit()
            flash("book was added successfully")

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
       user = session.get("user-id")

       if "user-id" not in session:
           flash("please login to checkout a book")

           return redirect(f"/book/{id}")
       
       
       issued_book = Copy.query.filter_by(issued_by=user).first()
       if issued_book:
             flash("You can only borrow one book at a time.")
             return redirect(f"/book/{id}")

       if book_id:

           if book_id.present_copy > 0:
                copy = Copy(issued_by=session.get("user-id"), date_issued=datetime.now(),
                   date_return=datetime.now() + timedelta(days=7), book=book_id.id)

                book_id.present_copy -= 1
                book_id.issued_copy += 1
                db.session.add(book_id)
                db.session.commit()

                db.session.add(copy)
                db.session.commit()

                flash("checkout successfully")

           else:
               flash("book is unavaliable")

       return redirect("/book/issued/view")


@app.route("/book/issued/view")
def issued_book_info():

    if "user-id" not in session:

        return redirect("/")

    book_1 = Copy.query.filter_by(issued_by=session.get("user-id")).first()

    return render_template("book/issued_book_info.html", book_1=book_1)


@app.route("/books/issued")
def issue_book():

    if "admin_num" not in session:
        return redirect("/")

    all_issued_book = Copy.query.all()

    return render_template("admin/issued.html", all_issued_book=all_issued_book)


@app.route("/book/<int:id>/return", methods=["GET", "POST"])
def return_book(id):

    if "user-id" not in session:
        flash("You must be logged in to return a book.")
        return redirect("/login")

    book_id = Copy.query.filter_by(
        book=id, issued_by=session["user-id"]).first()

    if book_id:
            book = Book.query.get(id)

            if book:

                    book.present_copy += 1
                    book.issued_copy -= 1

                    book_id.date_return = datetime.now()
                    
                    
                    db.session.delete(book_id)
                    db.session.commit()

      
                    flash("return book successfully")
      
                    return redirect("/book/issued/view")
      
  
  
    
@app.route("/admin/logout")
def addmin_logout():
    
    session.pop("admin_num")
    
    return redirect("/")




@app.route("/logout")
def logout():
    session.pop("user-id")
    
    return redirect("/")







if __name__ == '__main__':
    app.run(debug=True)
    
    