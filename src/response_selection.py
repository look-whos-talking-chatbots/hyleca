"""
File that contains functions to perform the final response selection
"""

import spacy

SPACY_MODELS = {
    'en': spacy.load('en_core_web_lg')
}


def select_response(candidates_list, query, language):
    """Response selection module based on simple similarity scoring"""
    if len(candidates_list) < 2:
        return candidates_list
    else:
        query_vec = SPACY_MODELS[language](query)
        return [max([(candid, query_vec.similarity(SPACY_MODELS[language](candid['text'])))
                     for candid in candidates_list], key=lambda x: x[1])[0]]
