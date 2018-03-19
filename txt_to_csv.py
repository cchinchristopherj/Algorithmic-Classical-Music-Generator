'''
Usage:
python txt_to_csv.py
'''
# Converts given harmonic labels .txt file to a .csv file for further processing

import csv

with open('jsbach_chorales_harmony.txt') as input_file:
    lines = input_file.readlines()
    newlines = []
    for line in lines:
        newline = line.strip().split(',')
        newlines.append(newline)
        
with open('jsbach_chorales_harmony.csv') as test_file:
    file_writer = csv.writer(test_file)
    file_writer.writerows(newlines)

