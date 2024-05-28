"""
File that loads the action functions of the bots to the system
and contains the wrapper function to call them.
"""

import os
import sys

from src.data_operations import parse_variable, inject_variable
from src.settings import BOTS_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), BOTS_PATH))

ACTION_INDEX = {}
for module in os.listdir(BOTS_PATH):
    if '.py' in module or '.git' in module or module == '__pycache__':
        continue
    mod = __import__(module, globals(), locals(), ['ACTION_INDEX'], 0)
    try:
        ACTION_INDEX.update(mod.ACTION_INDEX)
    except AttributeError:
        print("Cannot import the ACTION_INDEX from the __init__.py of the module named '" + module + "'")


def run_actions(user, state_obj, timing):
    if 'actions' in state_obj and state_obj['actions']:

        for action in state_obj['actions']:

            function = action[0]
            var_path = action[1]
            action_timing = action[2]

            if action_timing != timing:
                continue

            try:
                calculation = ACTION_INDEX[function](user)
            except:
                calculation = None

            user = inject_variable(user, var_path, calculation)

    return user
