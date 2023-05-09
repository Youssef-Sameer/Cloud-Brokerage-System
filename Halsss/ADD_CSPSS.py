from flask import Flask, render_template, request
import csv
from db import mysql
from db import cursor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csv_data']
    if not file:
        return render_template('index.html', error='No file selected')
    stream = stream.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    header = next(csv_input)
    rows = []
    for row in csv_input:
        rows.append(row)
    # convert rows to list of lists of converted values
    converted_rows = []
    for row in rows:
        converted_row = string_to_num(row)
        converted_rows.append(converted_row)
    # insert converted rows into database
    for i, row in enumerate(converted_rows):
        values_str = ",".join(str(val) for val in row)
        id = request.form['id{}'.format(i)] # get id from HTML form
        query = f"UPDATE cloud_provider SET performance_score='{values_str}' WHERE id={id}"
        cursor.execute(query)
        mysql.commit()
    cursor.close()
    mysql.close()
    return render_template('index.html', success='CSV file successfully uploaded and saved to database.')

def string_to_num(input_list):
    output_list = []
    for string in input_list:
        string = string.replace("\xa0", "")
        if string.lower() in ["yes", "aes", "aes256"]:
            output_list.append(1)
        elif string.lower() in ["no", "not mentioned"]:
            output_list.append(0)
        elif string.lower() in ["2048", "yes-annually"]:
            output_list.append(0.2)
        elif string.lower() in ["csp-responsibility", "56"]:
            output_list.append(0.3)
        elif string.lower() in ["sha256", "yes-bi-annually"]:
            output_list.append(0.4)
        elif string.lower() in ["3des", "rsa"]:
            output_list.append(0.5)
        elif string.lower() in ["csc-responsibility", "128", "3072", "yes-half-annually"]:
            output_list.append(0.6)
        elif string.lower() in ["sha384", "yes-quarterly"]:
            output_list.append(0.8)
        elif string.lower() in ["shared csp and csc responsibility", "256"]:
            output_list.append(0.9)
        else:
            try:
                output_list.append(float(string))
            except ValueError:
                output_list.append(string)
    return output_list

if __name__ == '__main__':
    app.run(debug=True)