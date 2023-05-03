from flask import Blueprint, render_template, request, redirect, session, url_for, flash
my_blueprint = Blueprint('my_blueprint', __name__)
import mysql.connector
from ADD_CSPSS import string_to_num

# Configure MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="cab"
)
# Create a cursor to execute SQL statements
cursor = mydb.cursor()

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
    return render_template('forgetpassword1.html')

@my_blueprint.route('/level1', methods=['POST', 'GET'])
def level1():
    return render_template('level1.html')

@my_blueprint.route('/level2', methods=['POST', 'GET'])
def level2():
    return render_template('level2.html')

@my_blueprint.route('/level3', methods=['POST', 'GET'])
def level3():
    return render_template('level3.html')

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
            return render_template('signup1.html', error=error)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE user_email=%s", (email,))
        user = cursor.fetchone()
        if user is not None:
            error = 'Email already exists'
            return render_template('signup1.html', error=error)

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
        return render_template('signup1.html')



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
    file = request.files['file']
    if not file:
        return 'No file uploaded.'
    with open(file.filename, 'r', encoding='utf-8-sig') as csv_file, open('performance_matrix.txt', 'a') as txt_file, open('alternatives.txt', 'a') as alt_file:
        for line in csv_file:
            row = line.strip().split(',')
            alt_file.write(row[0] + '\n')
            output_list = string_to_num(row[1:])
            txt_file.write(','.join(map(str, output_list)) + '\n')
    return 'File uploaded.'

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

