"""
File that contains function to call natural language generation models.
"""

import re
import backoff
import openai

from .settings import OPENAI_APIKEY


def generate_gpt_chat_response(chat_history, model_name='GPT-3.5-turbo'):

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=3, factor=3)
    def generation_request(**kwargs):
        return openai.ChatCompletion.create(**kwargs)

    openai.api_key = OPENAI_APIKEY
    messages = [{
        'role': 'system',
        'content': 'you should NEVER ask questions.'
    }]
    messages += [
        {
            "role": "assistant" if utterance['bot'] else "user",
            "content": utterance['text']
        }
        for utterance in chat_history
        if ('generator' not in utterance  # this if-statement prevents sending utterances from other NLGs and human
            or utterance['generator'].lower() in ['human', '-', model_name.lower()])
    ]

    try:
        response = generation_request(model=model_name.lower(),
                                      messages=messages,
                                      max_tokens=100)
    except openai.error.RateLimitError:
        return {}

    text = response['choices'][0]['message']['content']

    # It is advisable to remove the question from the generated content
    # This is because the HyLECA system is built to moderate the dialogues by pre-scripting the questions.
    text = re.sub(r"([^\n?!.]*\?\s*)", "", text)

    return {
        'text': text.strip(),
        'utterance_type': 'responses',
        'generator': model_name,
        'metadata': response
    }
