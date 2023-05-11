import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="sql7.freesqldatabase.com",
  user="sql7617565",
  password="E4eMPK6xlF",
  database="sql7617565"
)
# Create a cursor to execute SQL statements
cursor = mydb.cursor()


performance_matrix_query = "SELECT performance_score FROM level1"
cursor.execute(performance_matrix_query)
performance_matrix_result = cursor.fetchall()
performance_matrix1 = np.array([list(map(float, row[0].split(','))) for row in performance_matrix_result])

performance_matrix_query = "SELECT performance_score FROM level2"
cursor.execute(performance_matrix_query)
performance_matrix_result = cursor.fetchall()
performance_matrix2 = np.array([list(map(float, row[0].split(','))) for row in performance_matrix_result])

performance_matrix_query = "SELECT performance_score FROM cloud_provider"
cursor.execute(performance_matrix_query)
performance_matrix_result = cursor.fetchall()
performance_matrix3 = np.array([list(map(float, row[0].split(','))) for row in performance_matrix_result])

# Read in the list of alternatives from the MySQL database
alternatives_query = "SELECT csp_name FROM level1"
cursor.execute(alternatives_query)
alternatives_result = cursor.fetchall()
alternatives = [result[0] for result in alternatives_result]