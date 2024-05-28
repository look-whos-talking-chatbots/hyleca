"""
File contains functions to return corpus data to function the natural language understanding module.
"""

import os
import csv


def load_nlp_data(folder_path, file_name):
    with open(os.path.join(folder_path, file_name + '.csv'), mode='r')as file:
        csv_file = csv.reader(file)
        data_ = [{'text': line[0], 'label': line[1]}
                 for i, line in enumerate(csv_file)
                 if i != 0]
    return data_
