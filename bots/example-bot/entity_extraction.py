"""
File contains the common entity extraction functions.

The functions under this file should always expect "user_input" and "language" as their input.
They should always return a single variable, but the type of the variable can be integer, string, boolean, and None
depending on your application.
"""

import re
import spacy

from .corpus import NAME_PHRASES

SPACY_MODELS = {
    'en': spacy.load('en_core_web_lg')
}


def extract_numbers(query):
    """Extract numbers from a given plain text.

    :param string query: user input
    :return integer: the first of the detected numbers in the text
    """
    query = query.lower()
    number_matches = []

    # Any digit is added to the candidates list
    number_matches += re.findall(r'\d+', query)

    # Convert the string numbers to integers
    number_matches = [int(nm) for nm in number_matches]

    if len(number_matches):
        return number_matches
    else:
        return []


def extract_first_number(user_input, language):
    user_input = user_input.lower()
    entity = extract_numbers(user_input)
    if len(entity) > 0:
        entity = entity[0]
    return entity


def get_entire_user_input(user_input, language):
    return user_input


def extract_name(user_input, language):

    text_modifier = {
        'en': 'My name is '
    }

    if len(user_input.split()) == 1:
        user_input = text_modifier[language] + user_input

    # Attempt to increase the precision by making the user's name title case
    if any(phrase.lower() in user_input.replace('\'', '') for phrase in NAME_PHRASES[language]):
        user_input = ' '.join(user_input.split()[:-1]) + ' ' + user_input.split()[-1].title()

    name = ''
    doc = SPACY_MODELS[language](user_input)
    if len(doc.ents) > 0:
        name = doc.ents[0].text.title()

    return name


def extract_participant_id(query, language):
    query = query.lower()

    participant_id = None

    # Any digit is added to the candidates list
    number_matches = re.findall(r'\b\d{4}\b', query)

    if number_matches:
        participant_id = str(number_matches[0])

    return participant_id
