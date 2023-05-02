from flask import Blueprint, render_template

my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@my_blueprint.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@my_blueprint.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template('contact.html', methods=['POST', 'GET'])

@my_blueprint.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    return render_template('forgetpassword1.html')

@my_blueprint.route('/level1', methods=['POST', 'GET'])
def level1():
    return render_template('level1.html')

@my_blueprint.route('/level2', methods=['POST', 'GET'])
def level2():
    return render_template('level2.html', methods=['POST', 'GET'])

@my_blueprint.route('/level3', methods=['POST', 'GET'])
def level3():
    return render_template('level3.html')

@my_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login1.html', methods=['POST', 'GET'])

@my_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('Signup1.html', methods=['POST', 'GET'])
