from flask import Blueprint, render_template, request, redirect, session
my_blueprint = Blueprint('my_blueprint', __name__)
import mysql.connector

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
            return render_template('index.html')
        else:
            error = 'Invalid email or password'
            return render_template('login1.html', error=error)
    else:
        return render_template('login1.html')

@my_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('Signup1.html')


@my_blueprint.route('/myprofile', methods=['POST', 'GET'])
def myprofile():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    user_email = session.get('user_email')
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template('My_profile.html', userdata=user)
