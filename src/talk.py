"""
File that contains the main wrapper function for talking to the bots.
"""

from src.data_operations import are_conditions_met
from src.generation_module import GENERATION_INDEX
from src.nlu import run_actions, extract_information, text_categorisation, multiple_choice
from src.response_selection import select_response
from src.retrieval_module import get_state_utterances, select_retrieval_utterance, \
    fill_static_slots, fill_retrieval_slots
from src.state_handler import get_current_flow, get_current_state, process_trigger


def talk(user, bot, user_input, history=None):
    history = [] if history is None else history

    dialogue_flows = bot.dialogue_flows
    slot_fillers = bot.slot_fillers

    # Fetch current Flow and State
    flow_obj = get_current_flow(user, dialogue_flows)
    state_obj = get_current_state(user, flow_obj)

    outputs = []
    trigger_next_state = False

    if state_obj['type'] == "on-hold":

        # Entity Extraction
        user = extract_information(user, state_obj, user_input, bot.language)
        # Text Classification
        user = text_categorisation(user, state_obj, user_input, bot.language)
        # Multiple Choice Question
        user = multiple_choice(user, state_obj, user_input)

        # Run the actions that was designed to be run if the state repeats itself
        user = run_actions(user, state_obj, 'pre')
        user = run_actions(user, state_obj, 'repeat')

        state_utterances = get_state_utterances(user, state_obj, 'responses')

        if state_utterances:
            output = state_utterances[0]
            output['text'] = fill_static_slots(output['text'], user, slot_fillers)
            output['text'] = fill_retrieval_slots(user_input, output['text'], user,
                                                  slot_fillers, language=bot.language)
            output['flow_id'] = flow_obj['id']
            output['state_id'] = state_obj['id']
            outputs.append(output)

        trigger_candidates = [trigger
                              for trigger in state_obj['triggers']
                              if are_conditions_met(user, trigger['conditions'])]

        # Important: In an on-hold state, always trigger the first available option
        trigger = trigger_candidates[0]['trigger']

        # Process the trigger only if the current state id is not equal to the destination state id,
        if (user['progress']['state']['current'] != trigger[1]
                and user['progress']['flow']['current'] != trigger[1]):

            # Run the actions that was designed to be run only if the state is actually ending
            user = run_actions(user, state_obj, 'post')

            user = process_trigger(trigger, user, dialogue_flows, flow_obj)
            if trigger[1] != 10000:
                trigger_next_state = True

    elif state_obj['type'] == "monologue":

        user = run_actions(user, state_obj, 'pre')
        user = run_actions(user, state_obj, 'repeat')

        state_utterances = get_state_utterances(user, state_obj, 'responses')

        for output in state_utterances:
            output['text'] = fill_static_slots(output['text'], user, slot_fillers)
            output['text'] = fill_retrieval_slots(user_input, output['text'], user,
                                                  slot_fillers, language=bot.language)
            output['flow_id'] = flow_obj['id']
            output['state_id'] = state_obj['id']
            outputs.append(output)

        # Run the actions that was designed to be run only if the state is actually ending
        user = run_actions(user, state_obj, 'post')

        trigger_candidates = [trigger
                              for trigger in state_obj['triggers']
                              if are_conditions_met(user, trigger['conditions'])]

        # Important: In a monologue state, always trigger the first available option
        trigger = trigger_candidates[0]['trigger']

        user = process_trigger(trigger, user, dialogue_flows, flow_obj)
        if trigger[1] != 10000:
            trigger_next_state = True

    if state_obj['type'] == "dialogue":

        # Entity Extraction
        user = extract_information(user, state_obj, user_input, bot.language)
        # Text Classification
        user = text_categorisation(user, state_obj, user_input, bot.language)
        # Multiple Choice Question
        user = multiple_choice(user, state_obj, user_input)

        # Run the actions that was designed to be run if the state repeats itself
        user = run_actions(user, state_obj, 'repeat')

        # Run the actions that was designed to be run only if the state is completely new
        if not user['progress']['state']['question']['isAsked']:
            user = run_actions(user, state_obj, 'pre')

        # If the next utterance needs to be a question:
        if user['progress']['state']['question']['isNext']:

            if not user['progress']['state']['question']['isAsked']:
                candidate_utterances = get_state_utterances(user, state_obj, 'questions')
            else:
                # If questions are already asked, do not ask it again
                candidate_utterances = [{
                    'text': '',
                    'utterance_type': 'questions',
                    'generator': 'human'
                }]

            user['progress']['state']['question']['isNext'] = False
            user['progress']['state']['question']['isAsked'] = True
            user['progress']['state']['exchangeCounter'] = 0

        # If the next utterance needs to be a reflection:
        else:
            user['progress']['state']['exchangeCounter'] += 1

            state_utterances = get_state_utterances(user, state_obj, 'responses')

            for utterance in state_utterances:
                utterance['text'] = fill_static_slots(utterance['text'], user, slot_fillers)

            # Reduce the human-authored utterance to one by information retrieval
            retrieved_utterance = select_retrieval_utterance(user_input, state_utterances, user,
                                                             slot_fillers, language=bot.language)

            state_generators = []
            if 'generators' in state_obj:
                if 'all' in state_obj['generators']:
                    state_generators = GENERATION_INDEX.values()
                else:
                    state_generators = [nlg_model
                                        for nlg_id, nlg_model in GENERATION_INDEX.items()
                                        if nlg_id.lower() in state_obj['generators']]

            generated_utterances = []
            for generation_function in state_generators:
                generation_response = generation_function(history)
                if generation_response:
                    generated_utterances.append(generation_response)

            candidate_utterances = [retrieved_utterance] + generated_utterances

        candidate_utterances = select_response(candidate_utterances,
                                               query=user_input,
                                               language=bot.language)

        for output in candidate_utterances:
            output['text'] = fill_static_slots(output['text'], user, slot_fillers)
            output['flow_id'] = flow_obj['id']
            output['state_id'] = state_obj['id']
            outputs.append(output)

        # Note: Exchange counter counts how many times the user interacted with the bot within a single state.
        #       If the exchange counter is zero, it means so far only the chatbot talked since the state has
        #       started. In a dialogue state, only trigger the next state if the user has responded at least once.
        if user['progress']['state']['exchangeCounter'] != 0:

            trigger_candidates = [trigger
                                  for trigger in state_obj['triggers']
                                  if are_conditions_met(user, trigger['conditions'])]

            trigger = trigger_candidates[0]['trigger']

            # Process the trigger only if the current state id is not equal to the destination state id
            if user['progress']['state']['current'] != trigger[1]:

                # Run the actions that was designed to be run only if the state is actually ending
                user = run_actions(user, state_obj, 'post')

                user = process_trigger(trigger, user, dialogue_flows, flow_obj)
                if trigger[1] != 10000:
                    trigger_next_state = True

            else:
                # If the state is going to stay the same, do not ask the same question
                user['progress']['state']['question']['isAsked'] = True

    return outputs, user, trigger_next_state
