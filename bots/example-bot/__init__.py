"""
Contains the indices for the functions belong to this bot
"""

import os

from .actions import *
from .entity_extraction import *
from .text_categorisation import *
from .generation_models import *

FLOWS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flows')

AGENT_INDEX = {
    'example-bot': {
        'path': 'example_bot_flows',  # The name of the corresponding JSON file within the flows/ folder
        'generators': None,  # Give a list here if the bot should utilize generation models.
        'onhold_duration': 10,  # How long should the bot wait between its sessions (in seconds)
    },
    'example-bot-generative': {
        'path': 'example_bot_flows',
        'generators': ['gpt35'],  # within this list use the ids from GENERATION_INDEX.
        'onhold_duration': 10,
    }
}

CATEGORISATION_INDEX = {
    'placeholder': categorize_placeholder,
    'yes_no': categorize_yes_no,
}

ENTITY_EXTRACTION_INDEX = {
    'user_input': get_entire_user_input,
    'numbers': extract_first_number,
    'name': extract_name,
    'participant_id': extract_participant_id,
}

ACTION_INDEX = {
    'get_on_hold': get_on_hold,
    'set_on_hold_time': get_now_time,
    'set_on_hold_true': get_true
}

GENERATION_INDEX = {
    'gpt35': generate_gpt_chat_response,
}
