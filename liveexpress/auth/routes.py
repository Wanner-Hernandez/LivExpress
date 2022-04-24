from flask import render_template,url_for,flash,redirect,request,Blueprint,jsonify
from liveexpress.auth.forms import RegistrationForm,LoginForm
from liveexpress.models import User
from liveexpress import db,bcrypt
from . import auth
from flask_login import login_user,current_user,logout_user,login_required

LOGGEDIN=False


@auth.route("/register",methods=["GET","POST"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        phone=request.form.get("phone")
        uname=form.username.data
        email=form.email.data
        lname=form.lname.data
        fname=form.fname.data
        p1=form.password.data
        p2=form.confirm_password.data
        gender=form.gender.data
        password=form.password.data
        hashed_password=bcrypt.generate_password_hash(
            password).decode("utf-8")

        error=None

        user=User(phone_number=phone,username=uname,fname=fname,
                  lname=lname,gender=gender,email=email,password=hashed_password)

        if len(password) < 12 or not any(letter.islower() for letter in password) or \
                not any(letter.isupper() for letter in password) or \
                not any(letter.isdigit() for letter in password) or \
                not any(letter in "@$#:%&!*$" for letter in password):
            flash("Password should include at least 12 characters in length, and include at least 1 uppercase character, 1 lowercase character, 1 number and 1 special character")
            return render_template("register.html", title="Registration",form=form)

            #                ,msg="""Password should include at least
            # 12 characters in length, and
            # include at least 1 uppercase character,
            # 1 lowercase character, 1 number and 1 special character""")

        # if error is None:
        #     user=User(phone_number=phone,username=uname,fname=fname,
        #               lname=lname,gender=gender,email=email,password=hashed_password)

        if error is None:

            db.session.add(user)
            db.session.commit()

            flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('auth.login'))

    return render_template('register.html',title="Registration",form=form)


@auth.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        # return redirect(url_for('main.home'))
        pass
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash("You are now logged in",'success')
            return redirect(next_page) if next_page else redirect(url_for('main.feed'))
        else:
            flash('Login Unsuccessful. Please check Username and password','danger')
    return render_template('login.html',title='Login',form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You are now logged out.",'warning')
    return redirect(url_for('main.index'))
