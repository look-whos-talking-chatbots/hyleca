import os
import yaml

CONFIG_PATH = os.environ.get('CONFIG_PATH')

# Loading the data inside config file.
with open(CONFIG_PATH, 'r') as file:
    data = yaml.safe_load(file)

PROJECT_PATH = data['paths']['project']

del data
