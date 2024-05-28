"""
File that contains functions to generate utterances with natural language generation models
"""

import os
import sys

from src.settings import BOTS_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), BOTS_PATH))

GENERATION_INDEX = {}
for module in os.listdir(BOTS_PATH):
    if '.py' in module or '.git' in module or module == '__pycache__':
        continue
    mod = __import__(module, globals(), locals(), ['GENERATION_INDEX'], 0)
    try:
        GENERATION_INDEX.update(mod.GENERATION_INDEX)
    except AttributeError:
        print("Cannot import the GENERATION_INDEX from the __init__.py of the module named '", module, "'")
