from flask import Flask, render_template, request, url_for
import numpy as np
from db import performance_matrix, alternatives


criteria = ["Data Encryption at rest","Encryption Algorithm","Key size","Key Generation","Key Inventory Management","Data Inventory","Data Classification","Data encryption in Transit","Encryption in Transit algorithm(RSA)","Key size","Data Retention and Deletion","Sensitive Data Protection","Infrastructure and Virtualization Security Policy and Procedures","Network Security 1","Network Security 2","Network Security 3","Network Security 4","Network Defense"]

def model():
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
