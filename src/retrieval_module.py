"""
File that contains functions to process human-authored retrieved utterances
"""

import re
import random
import spacy

from .data_operations import check_condition, parse_variable, are_conditions_met

SPACY_MODELS = {
    'en': spacy.load('en_core_web_lg')
}


def get_state_utterances(user, state_obj, utterance_type):
    utterances_list = []

    for utterance in state_obj[utterance_type]:

        if are_conditions_met(user, utterance['conditions']):

            # If all the text options are already in the history do not check the history
            # skip_flag = False if all(text in history[-20:] for text in utterance['text']) else True

            for text in utterance['text']:
                # if skip_flag:
                #     # If there is text options that are not in the history:
                #     if text in [h['text'] for h in history[-20:]]:
                #         continue

                utt_obj = {
                    'text': text,
                    'utterance_type': utterance_type,
                    'generator': 'human'
                }

                utterances_list.append(utt_obj)

    return utterances_list


def get_filler_candidates(slot_fillers_, var_path_, user):
    candidates = []

    for utterance in slot_fillers_[var_path_]:
        if (all(check_condition(user, cond) for cond in utterance['conditions'])
                or len(utterance['conditions']) == 0):
            candidates += utterance['text']

    return candidates


def fill_static_slots(text, user, slot_fillers):
    """

    Note: There are three types of slot-fillers:
              1- variable slots = filled with information from user data,
              2- static slots = filled by one of the given texts, chosen at a random,
              3- retrieval slots = filled by one of the given texts chosen based on
                 its relation to the user input.

    :param text:
    :param user:
    :param slot_fillers:
    :return:
    """

    if '{{' in text and '}}' in text:

        for slot in re.findall(r"{{\s[a-zA-Z0-9_.-]+\s}}", text):

            value = None

            var_path = slot.split('{{')[1].split('}}')[0].strip()

            # Static slots are chosen at random
            if var_path in slot_fillers['static_slots']:
                # If the given variable path is in the static slot fillers:
                filler_candidates = get_filler_candidates(slot_fillers['static_slots'], var_path, user)
                if len(filler_candidates) > 0:
                    value = random.choice(filler_candidates)

            else:
                # Else look for the variable path within the user profile data
                value = parse_variable(user, var_path)

            if value is not None:
                text = text.replace(slot, str(value))

    return text


def retrieval_model(query, candidate_texts, language='en'):
    if not candidate_texts:
        return {
            'text': '',
            'utterance_type': 'responses',
            'generator': 'human'
        }
    else:
        query_vec = SPACY_MODELS[language](query)
        return max([(candid, query_vec.similarity(SPACY_MODELS[language](candid)))
                    for candid in candidate_texts], key=lambda x: x[1])[0]


def fill_retrieval_slots(user_input, text, user, slot_fillers, language='en'):

    if '{{' in text and '}}' in text:

        for slot in re.findall(r"{{\s[a-zA-Z0-9_.-]+\s}}", text):

            var_path = slot.split('{{')[1].split('}}')[0].strip()

            # # Fillers for the retrieval slots are chosen by the retrieval model
            if var_path in slot_fillers['retrieval_slots']:
                # If the given variable path is in the static slot fillers:
                filler_candidates = get_filler_candidates(slot_fillers['retrieval_slots'], var_path, user)
                value = retrieval_model(user_input, filler_candidates, language)
            else:
                value = ''

            if value is None:
                value = ''

            text = text.replace(slot, str(value))

    return text


def select_retrieval_utterance(user_input, candidates_list, user, slot_fillers, language='en'):

    candidate_texts = []
    for utterance in candidates_list:
        utterance['text'] = fill_retrieval_slots(user_input, utterance['text'], user, slot_fillers, language)
        candidate_texts.append(utterance['text'])

    selected_text = retrieval_model(user_input, candidate_texts, language)

    selection = [selection for selection in candidates_list
                 if selection['text'] == selected_text]

    if selection:
        selection = selection[0]
    else:
        selection = random.choice(candidates_list)

    return selection
