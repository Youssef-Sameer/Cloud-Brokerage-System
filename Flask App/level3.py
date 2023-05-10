from flask import Flask, render_template, request, url_for
import numpy as np
from db import performance_matrix3, alternatives

# Define a dictionary that maps the string choices to their corresponding numerical values
choice_map = {
    # change this
    "yes":0.05,
    "no":0,
    "Triple-Des 56":0.01,
    "AES 128":0.03,
    "AES 256":0.05,
    "Weekly":0.11,
    "Monthly":0.09,
    "Bi-Monthly":0.07,
    "Quarterly":0.05,
    "Annually":0.03,
    "biennial":0.01,
    "2048":0.01,
    "3072":0.03,
    "RSA+sha256":0.06,
    "4096":0.09,
    "solely responsible":0.03,
    "shared responsible":0.06,
    "CSP responsible":0.09,
    
    
    
}

def level3form():
    if request.method == 'POST':
        # Read the criteria weights and choices from the form
        
        choices = request.form.getlist('choices')
        print(choices)

        # Convert the choices to their corresponding numerical values
        choices_values = [choice_map[choice] for choice in choices]

        # Normalize the performance matrix
        normalized_matrix = performance_matrix3 / performance_matrix3.sum(axis=0)

        # Calculate the weighted normalized matrix
        weighted_matrix = normalized_matrix * choices_values

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
        return render_template('level3.html')

