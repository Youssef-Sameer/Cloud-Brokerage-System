from flask import Flask, render_template, request, url_for
from views import my_blueprint

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'KLMMDSKCKSL8465-8451adsvdsklmklamdsak'
app.register_blueprint(my_blueprint)
if __name__ == '__main__':
    app.run(debug=True)