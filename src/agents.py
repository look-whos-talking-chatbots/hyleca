"""
File that loads the data of the bots to the system
and contains the wrapper function to load them as Bot objects.
"""

import os
import sys

from src.bot import Bot
from src.settings import BOTS_PATH

sys.path.append(os.path.join(os.path.dirname(__file__), BOTS_PATH))

AGENT_INDEX = {}
for module in os.listdir(BOTS_PATH):
    if '.py' in module or '.git' in module or module == '__pycache__':
        continue
    mod = __import__(module, globals(), locals(), ['AGENT_INDEX', 'FLOWS_PATH'], 0)
    try:
        # Enrich the agent index with the absolute file path for the flows
        for token, agent in mod.AGENT_INDEX.items():
            file_path = os.path.join(mod.FLOWS_PATH, agent['path'])
            if not file_path.endswith('.json'):
                file_path += '.json'
            mod.AGENT_INDEX[token]['path'] = file_path

        AGENT_INDEX.update(mod.AGENT_INDEX)
    except AttributeError:
        print("Cannot import the AGENT_INDEX from the __init__.py of the module named '", module, "'")


def get_bot(bot_token):
    return Bot.load_bot(AGENT_INDEX[bot_token])
