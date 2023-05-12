import csv  
import tkinter as tk
from tkinter import filedialog

def string_to_num(input_list):
    output_list = []
    for string in input_list:
        string = string.replace("\xa0", "")
        if string.lower() in ["Yes", "yes","RSA4096","Monthly"]:
            output_list.append(1)
        elif string.lower() in ["No", "no","RSAnotmentioned"]:
            output_list.append(0)
        elif string.lower() in ["730"]:
            output_list.append(0.15)
        elif string.lower() in ["Annually",]:
            output_list.append(0.2)
        elif string.lower() in ["RSA2048"]:
            output_list.append(0.25)
        elif string.lower() in ["CSC-responsibility","3DES56","365"]:
            output_list.append(0.3)
        elif string.lower() in ["Bi-annually"]:
            output_list.append(0.4)
        elif string.lower() in ["90"]:
            output_list.append(0.45)
        elif string.lower() in ["RSA3072"]:
            output_list.append(0.5)
        elif string.lower() in ["SharedCSPandCSCresponsibility","AES128","Half-annually","60"]:
            output_list.append(0.6)
        elif string.lower() in ["RSA+sha256","30"]:
            output_list.append(0.75)
        elif string.lower() in ["Quarterly"]:
            output_list.append(0.8)
        elif string.lower() in ["CSP-responsibility","AES256","7"]:
            output_list.append(0.9)
        else:
            try:
                output_list.append(float(string))
            except ValueError:
                output_list.append(string)
    return output_list
