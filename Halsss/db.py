from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask (__name__)


app.config['MYSQL_HOST'] = 'localhost'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'boda'  # Replace with your MySQL database name

mysql = MySQL (app)