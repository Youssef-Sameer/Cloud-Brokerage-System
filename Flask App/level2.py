from flask import Flask, render_template, request, url_for
import numpy as np
from db import performance_matrix2, alternatives

# Define a dictionary that maps the string choices to their corresponding numerical values
choice_map = {
    "Strong": 0.166,
    "Medium": 0.116,
    "Weak": 0.086,
    "Yes": 0,
    "No": 0,
    
}

def level2form():
    if request.method == 'POST':
        # Read the criteria weights and choices from the form
        
        choices = request.form.getlist('choices')
        print(choices)

        # Convert the choices to their corresponding numerical values
        choices_values = [choice_map[choice] for choice in choices]

        # Normalize the performance matrix
        normalized_matrix = performance_matrix2 / performance_matrix2.sum(axis=0)

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
        return render_template('level2.html')

