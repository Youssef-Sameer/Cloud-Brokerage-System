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

@my_blueprint.route('/addcsp', methods=['POST', 'GET'])
def addcsp():
    if request.method == 'POST':
        # Get form data
        cloud_provider_name = request.form['cloud_provider']
        website = request.form['Website']
        Level1Score = request.form['Level1Score']
        Level2Score = request.form['Level2Score']
        Level3Score = request.form['Level3Score']
        
        cursor.execute("INSERT INTO level1 (csp_name, website, performance_score) VALUES (%s, %s, %s)", (cloud_provider_name, website, Level1Score))
        cursor.execute("INSERT INTO level2 (csp_name, website, performance_score) VALUES (%s, %s, %s)", (cloud_provider_name, website, Level2Score))
        cursor.execute("INSERT INTO cloud_provider (csp_name, website, performance_score) VALUES (%s, %s, %s)", (cloud_provider_name, website, Level3Score))
        mydb.commit()
        
        return render_template('admin_panel_view_csp.html')
    else:
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
    if request.method == 'POST':
        # Handle the form submission
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        resume_link = request.form['resume_link']
        relevant_experience = request.form['relevant_experience']

        # Insert the data into the apply_csp table
        cursor.execute("INSERT INTO apply_csp (name, email, phonenumber, link, CAIQ_link) VALUES (%s, %s, %s, %s, %s)", (name, email, phone, resume_link, relevant_experience))
        mydb.commit()

        # Return a response to indicate that the form was submitted successfully
        return 'Form submitted successfully!'
    else:
        # Render the form template
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

@my_blueprint.route('/delete_apply_csp/<int:apply_csp_id>', methods=['GET', 'POST'])
def delete_apply_csp(apply_csp_id):
    cursor.execute("DELETE FROM apply_csp WHERE id=%s", (apply_csp_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.Newcspadmin'))

@my_blueprint.route('/delete_contact/<int:contact_id>', methods=['GET', 'POST'])
def delete_contact(contact_id):
    cursor.execute("DELETE FROM contact WHERE id=%s", (contact_id,))
    mydb.commit()
    return redirect(url_for('my_blueprint.review'))
@my_blueprint.route('/editprofile', methods=['POST', 'GET'])
def editprofile():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('my_blueprint.login'))

    # Get the current user's data
    user_id = session['user_id']
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    userdata = cursor.fetchone()

    if request.method == 'POST':
        # Retrieve the updated username from the form data
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        old_password = request.form.get('current_password')
        
        # Update the user's profile in the database
        cursor.execute("SELECT user_password FROM users WHERE id = %s", (user_id,))
        current_password=cursor.fetchone()
        if current_password[0]!=old_password:
            error = 'Current password is wrong'
            return render_template('edit_profile.html',userdata=userdata,error=error)
        else:
            cursor.execute("UPDATE users SET user_name = %s ,user_password = %s WHERE id = %s", (username, new_password, user_id,))
            mydb.commit()
            return redirect(url_for('my_blueprint.myprofile'))
    else:
        # Render the edit profile page with the current username
        return render_template('edit_profile.html',userdata=userdata)
    
@my_blueprint.route('/history', methods=['POST', 'GET'])
def history():
    user_id = session['user_id']
    cursor.execute("SELECT ranking FROM history WHERE user_id=%s ORDER BY id DESC LIMIT 1", (user_id,))
    choice = cursor.fetchone()
    if choice is not None:
        choicess = choice[0].split(',')
    else:
        choicess = []
    return render_template('history.html', ranking=choicess)
@my_blueprint.route('/Newcspadmin', methods=['POST', 'GET'])
def Newcspadmin():
        # Insert the data into the apply_csp table
        cursor.execute("SELECT * FROM apply_csp")
        users=cursor.fetchall()
        # Render the form template
        return render_template('New_csp_admin.html',users=users)







