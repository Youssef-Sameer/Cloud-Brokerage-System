import csv
import tkinter as tk
from tkinter import filedialog

def string_to_num(input_list):
    output_list = []
    for string in input_list:
        string = string.replace("\xa0", "")
        if string.lower() in ["yes", "AES", "aes","Aes256","AES256","Yes","YES","4096","yes-monthly","yes- monthly","Yes-monthly","Yes- monthly","yes- monthly","Yes- monthly","RSA+sha","rsa+sha","RSA+SHA"]:
            output_list.append(1)
        elif string.lower() in ["No", "no", "Not mentioned","not mentioned","Not Mentioned","notmentioned"]:
            output_list.append(0)
        elif string.lower() in ["2048","yes-annually","yes- annually","Yes-annually","Yes- annually","yes- annually","Yes- annually"]:
            output_list.append(0.2)
        elif string.lower() in ["CSP-responsibility", "csp-responsibility", "csp responsibility", "CSP responsibility","56"]:
            output_list.append(0.3)
        elif string.lower() in ["Sha256","SHA256","sha256","sha-256","SHA-256","SHA-256","sha 256","SHA 256","SHA 256","yes-bi-annually","yes- bi-annually","Yes-bi-annually","Yes- bi-annually","yes- bi-annually","Yes- bi-annually"]:
            output_list.append(0.4)
        elif string.lower() in ["3DES", "3des", "3Des","RSA","rsa","Rsa"]:
            output_list.append(0.5)
        elif string.lower() in ["CSC-responsibility", "csc-responsibility", "csc responsibility", "CSC responsibility","128","3072","yes-half-annually","yes- half-annually","Yes-half-annually","Yes- half-annually","yes- half-annually","Yes- half-annually"]:
            output_list.append(0.6)
        elif string.lower() in ["sha384","SHA384","Sha384","sha-384","SHA-384","SHA-384","sha 384","SHA 384","SHA 384","yes-quarterly","yes- quarterly","Yes-quarterly","Yes- quarterly","yes- quarterly","Yes- Quarterly","yes- quarterly"]:
            output_list.append(0.8)
        elif string.lower() in ["Shared CSP and CSC responsibility", "shared csp and csc responsibility", "Shared csp and csc responsibility", "shared CSP and CSC responsibility","256"]:
            output_list.append(0.9)
        else:
            try:
                output_list.append(float(string))
            except ValueError:
                output_list.append(string)
    return output_list


def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    with open(file_path, 'r', encoding='utf-8-sig') as csv_file, open('performance_matrix.txt', 'a') as txt_file, open('alternatives.txt', 'a') as alt_file:
        for line in csv_file:
            row = line.strip().split(',')
            alt_file.write(row[0] + '\n')
            output_list = string_to_num(row[1:])
            txt_file.write(','.join(map(str, output_list)) + '\n')

    print("Output written to performance_matrix.txt")
if __name__ == "__main__":
    main()
