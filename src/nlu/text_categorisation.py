"""
File that loads the text categorisation functions of the bots to the system
and contains the wrapper function to call them.
"""

import os
import sys

from src.data_operations import parse_variable, inject_variable
from src.settings import BOTS_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), BOTS_PATH))

TEXT_CATEGORISATION = {}
for module in os.listdir(BOTS_PATH):
    if '.py' in module or '.git' in module or module == '__pycache__':
        continue
    mod = __import__(module, globals(), locals(), ['CATEGORISATION_INDEX'], 0)
    try:
        TEXT_CATEGORISATION.update(mod.CATEGORISATION_INDEX)
    except AttributeError:
        print("Cannot import the CATEGORISATION_INDEX from the __init__.py of the module named '" + module + "'")


def text_categorisation(user, state_obj, user_input, language='en'):
    if 'categories' in state_obj and state_obj['categories']:

        for intent_classif in state_obj['categories']:

            function = intent_classif[0]
            var_path = intent_classif[1]

            try:
                intent = TEXT_CATEGORISATION[function](user_input, language)
            except:
                intent = None

            # if the variable path ends with 'list' or 'List',
            # append the intent to that list and then send it to the user db
            if var_path.lower().endswith('list'):
                intent_list = parse_variable(user, var_path)
                intent_list = [] if intent_list is None else intent_list
                if intent is not None and intent not in intent_list:
                    intent_list.append(intent)
                intent = intent_list  # this a renaming to use the same code below for all cases

            if intent is not None:
                user = inject_variable(user, var_path, intent)

    return user


def test_text_categorisation(user_input, function_name, language):
    intent = TEXT_CATEGORISATION[function_name](user_input, language)
    return intent
