import csv
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import numpy as np
from db import cursor
from db import mydb
from level1 import level1form
from level2 import level2form
from level3 import level3form
# from ADD_CSPSS import string_to_num

my_blueprint = Blueprint('my_blueprint', __name__)
# Configure MySQL connection









@my_blueprint.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@my_blueprint.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@my_blueprint.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Insert new contact into database
        cursor.execute("INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
        mydb.commit()

        # Redirect to thank you page
        return render_template('thankyou.html')
    else:
        return render_template('contact.html')


@my_blueprint.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    return render_template('review.html')

@my_blueprint.route('/level1', methods=['POST', 'GET'])
def level1():
    return level1form()

@my_blueprint.route('/level2', methods=['POST', 'GET'])
def level2():
    return level2form()



@my_blueprint.route('/level3', methods=['POST', 'GET'])
def level3():
    return level3form()


@my_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE user_email=%s AND user_password=%s", (email, password))
        user = cursor.fetchone()
        if user is not None:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            session['user_type'] = user[4]
            return render_template('index.html')
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@my_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # Get form data
        type = "User"
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            error = 'Passwords do not match'
            return render_template('signup.html', error=error)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE user_email=%s", (email,))
        user = cursor.fetchone()
        if user is not None:
            error = 'Email already exists'
            return render_template('signup.html', error=error)

        # Insert new user into database
        cursor.execute("INSERT INTO users (user_name, user_email, user_password,user_type) VALUES (%s, %s, %s,%s)", (name, email, password,type))
        mydb.commit()

        # Log in user and redirect to index page
        session['user_id'] = cursor.lastrowid
        session['user_name'] = name
        session['user_email'] = email
        session['user_type'] = type
        return render_template('index.html')
    else:
        return render_template('signup.html')



@my_blueprint.route('/myprofile', methods=['POST', 'GET'])
def myprofile():
    user_id = session.get('user_id')
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template('My_profile.html', userdata=user)

@my_blueprint.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@my_blueprint.route('/adminpanel')
def adminpanel():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('admin_panel_users.html',users=users)
@my_blueprint.route('/review')
def review():
    cursor.execute("SELECT * FROM contact")
    users = cursor.fetchall()
    return render_template('review.html',users=users)

@my_blueprint.route('/addcsp')
def addcsp():
    return render_template('add_csp.html')

@my_blueprint.route('/viewcsp')
def viewcsp():
    cursor.execute("SELECT * FROM Cloud_provider")
    csps=cursor.fetchall()
    return render_template('admin_panel_view_csp.html',csps=csps)



@my_blueprint.route('/result')
def result():
    return render_template('result.html')
    
@my_blueprint.route('/csp_request', methods=['POST', 'GET'])
def csp_request():
    return render_template('csp_request.html')

@my_blueprint.route('/add_admin/<int:user_id>', methods=['POST'])
def add_admin(user_id):
    cursor.execute("UPDATE users SET user_type='Admin' WHERE id=%s", (user_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.adminpanel'))

@my_blueprint.route('/remove_admin/<int:user_id>', methods=['POST'])
def remove_admin(user_id):
    cursor.execute("UPDATE users SET user_type='User' WHERE id=%s", (user_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.adminpanel'))

@my_blueprint.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.adminpanel'))
@my_blueprint.route('/delete_contact/<int:contact_id>', methods=['GET', 'POST'])
def delete_contact(contact_id):
    cursor.execute("DELETE FROM contact WHERE id=%s", (contact_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.review'))





