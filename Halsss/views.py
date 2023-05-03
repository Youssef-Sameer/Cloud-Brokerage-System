import csv
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
import numpy as np
import mysql.connector
from ADD_CSPSS import string_to_num

my_blueprint = Blueprint('my_blueprint', __name__)
# Configure MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="cab"
)
# Create a cursor to execute SQL statements
cursor = mydb.cursor()


performance_matrix_query = "SELECT performance_score FROM cloud_provider"
cursor.execute(performance_matrix_query)
performance_matrix_result = cursor.fetchall()
performance_matrix = np.array([list(map(float, row[0].split(','))) for row in performance_matrix_result])

# Read in the list of alternatives from the MySQL database
alternatives_query = "SELECT csp_name FROM cloud_provider"
cursor.execute(alternatives_query)
alternatives_result = cursor.fetchall()
alternatives = [result[0] for result in alternatives_result]








@my_blueprint.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@my_blueprint.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@my_blueprint.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template('contact.html')

@my_blueprint.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    return render_template('forgetpassword.html')

@my_blueprint.route('/level1', methods=['POST', 'GET'])
def level1():
    return render_template('level1.html')

@my_blueprint.route('/level2', methods=['POST', 'GET'])
def level2():
    return render_template('level2.html')

@my_blueprint.route('/level2_2', methods=['POST', 'GET'])
def level2_2():
    return render_template('level2_2.html')

@my_blueprint.route('/level2_3', methods=['POST', 'GET'])
def level2_3():
    return render_template('level2_3.html')

@my_blueprint.route('/level3', methods=['POST', 'GET'])
def level3():
    return render_template('level3.html')

@my_blueprint.route('/level3-2', methods=['POST', 'GET'])
def level3_2():
    return render_template('level3_2.html')

@my_blueprint.route('/level3_3', methods=['POST', 'GET'])
def level3_3():
    return render_template('level3_3.html')

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

@my_blueprint.route('/addadmin')
def addadmin():
    return render_template('add_admin.html')

@my_blueprint.route('/addcsp')
def addcsp():
    return render_template('add_csp.html')

@my_blueprint.route('/viewcsp')
def viewcsp():
    cursor.execute("SELECT * FROM Cloud_provider")
    csps=cursor.fetchall()
    return render_template('admin_panel_view_csp.html',csps=csps)

@my_blueprint.route('/viewadmins')
def viewadmins():
    cursor.execute("SELECT * FROM users WHERE user_type='Admin'")
    admins=cursor.fetchall()
    return render_template('admins.html',admins=admins)

@my_blueprint.route('/result')
def result():
    return render_template('result.html')

@my_blueprint.route('/form', methods=['POST', 'GET'])
def form():
    criteria = ["Data Encryption at rest","Encryption Algorithm","Key size","Key Generation","Key Inventory Management","Data Inventory","Data Classification","Data encryption in Transit","Encryption in Transit algorithm(RSA)","Key size","Data Retention and Deletion","Sensitive Data Protection","Infrastructure and Virtualization Security Policy and Procedures","Network Security 1","Network Security 2","Network Security 3","Network Security 4","Network Defense"]
    if request.method == 'POST':
        # Read the criteria weights from the form
        weights = np.array(request.form.getlist('weight')).astype(float)

        # Normalize the performance matrix
        normalized_matrix = performance_matrix / performance_matrix.sum(axis=0)

        # Calculate the weighted normalized matrix
        weighted_matrix = normalized_matrix * weights

        # Calculate the ideal and negative ideal solutions
        ideal_solution = np.max(weighted_matrix, axis=0)
        negative_ideal_solution = np.min(weighted_matrix, axis=0)

        # Calculate the Euclidean distances of each alternative to the ideal and negative ideal solutions
        d_i = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1))
        d_j = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1))

        # Calculate the relative closeness of each alternative to the ideal solution
        relative_closeness = d_j / (d_i + d_j)

        # Rank the alternatives by their relative closeness to the ideal solution
        rankings = np.argsort(relative_closeness)[::-1]

        # Pass the length of the alternatives list to the results page
        num_alternatives = len(alternatives)

        # Return the rankings and length to the results page
        return render_template('results.html', alternatives=alternatives, rankings=rankings, num_alternatives=num_alternatives, relative_closeness=np.round(relative_closeness, 5))

    else:
        # Render the form page
        return render_template('form.html', criteria=criteria)

