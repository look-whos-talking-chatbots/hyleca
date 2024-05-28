"""
File that loads the entity extraction functions of the bots to the system
and contains the wrapper function to call them.
"""

import os
import sys

from src.data_operations import inject_variable
from src.settings import BOTS_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), BOTS_PATH))

ENTITY_EXTRACTION = {}
for module in os.listdir(BOTS_PATH):
    if '.py' in module or '.git' in module or module == '__pycache__':
        continue
    mod = __import__(module, globals(), locals(), ['ENTITY_EXTRACTION_INDEX'], 0)
    try:
        ENTITY_EXTRACTION.update(mod.ENTITY_EXTRACTION_INDEX)
    except AttributeError:
        print("Cannot import the ENTITY_EXTRACTION_INDEX from the __init__.py of the module named '" + module + "'")


def extract_information(user, state_obj, user_input, language='en'):
    if 'entities' in state_obj and state_obj['entities']:

        for entity_extraction in state_obj['entities']:

            function = entity_extraction[0]
            var_path = entity_extraction[1]

            try:
                entity = ENTITY_EXTRACTION[function](user_input, language)
            except:
                entity = None

            if entity == '' or entity == ' ' or entity == []:
                entity = None

            user = inject_variable(user, var_path, entity)

    return user


def test_entity_extraction(user_input, function_name, language):
    entity = ENTITY_EXTRACTION[function_name](user_input, language)
    return entity
