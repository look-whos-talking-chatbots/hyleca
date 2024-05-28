"""
Contains the code to load the required data from the configuration file and assign them to global variables
"""

import os
import yaml

# The following are the standard paths for the bot to find and use the models and the data
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CLASSIFIER_PATHS = os.path.join(BASE_PATH, 'models', '{}-classif/model-best')
NLP_DATA_PATH = os.path.join(BASE_PATH, 'nlp-data')

CONFIG_PATH = os.environ.get('CONFIG_PATH')

# Loading the data inside config file.
with open(CONFIG_PATH, 'r') as file:
    data = yaml.safe_load(file)

# READ THE DATA AND ASSIGN TO NECESSARY VARIABLES BELOW.
OPENAI_APIKEY = data['api_keys']['openai']

del data
