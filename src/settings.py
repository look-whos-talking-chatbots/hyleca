"""
Contains the code to load the required data from the configuration file and assign them to global variables
"""

import os
import yaml

CONFIG_PATH = os.environ.get('CONFIG_PATH')

# Loading the data inside config file.
with open(CONFIG_PATH, 'r') as file:
    data = yaml.safe_load(file)

# READ AND ASSIGN VARIABLES FROM THE CONFIG FILE
BOTS_PATH = data['paths']['bots']

del data
