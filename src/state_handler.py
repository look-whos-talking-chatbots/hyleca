"""
File that contains core state operation functions
"""

from src.data_operations import check_condition


def get_current_flow(user, dialogue_flows):
    flow_id = user['progress']['flow']['current']

    flow_candidates = [flow for flow in dialogue_flows if flow['id'] == flow_id]

    if len(flow_candidates) > 0:
        flow_obj = flow_candidates[0]
    else:
        print("Error: Requested flow (with flow_id = {}) cannot be found in the dialogue flows.".format(str(flow_id)))
        flow_obj = None

    return flow_obj


def get_current_state(user, flow_obj):
    state_id = user['progress']['state']['current']

    state_obj = [state for state in flow_obj['states'] if state['id'] == state_id][0]

    return state_obj


def get_candidate_states(flow_obj, user):
    if flow_obj is None:
        return []

    #  all state conditions has to be satisfied
    return [state['id']
            for state in flow_obj['states']
            if all(check_condition(user, cond)
                   for cond in state['conditions'])]


def find_flow_id(dialogue_flows, state_id):
    return [flow['id']
            for flow in dialogue_flows
            if state_id in [state['id']
                            for state in flow['states']]][0]


def trigger_state(user, state_id):
    # never add states of 9999 and 10000 flows to past
    if not user['progress']['state']['current'] >= 9999:
        user['progress']['state']['past'].append(user['progress']['state']['current'])

    # Set the requested state as the current state
    user['progress']['state']['current'] = state_id

    user['progress']['state']['exchangeCounter'] = 0
    user['progress']['state']['question']['isNext'] = True
    user['progress']['state']['question']['isAsked'] = False

    return user


def trigger_flow(user, dialogue_flows, flow_id):
    # never add the flow 10000 to the "past" as it is reserved for "on-hold" functionality.
    if user['progress']['flow']['current'] != 10000:
        user['progress']['flow']['past'].append(user['progress']['flow']['current'])

    # Set the requested flow as the current flow
    user['progress']['flow']['current'] = flow_id

    flow_obj = get_current_flow(user, dialogue_flows)
    state_candidates = get_candidate_states(flow_obj, user)

    if not state_candidates:
        print("Error: There are no state candidates for the requested flow (with flow_id = {}).".format(str(flow_id)))
    else:
        # Consider using the exhaustive search for states
        state_id = state_candidates[0]
        user = trigger_state(user, state_id)

    return user


def process_trigger(trigger, user_, dialogue_flows, flow_obj):
    type_ = trigger[0]
    destination_id = trigger[1]

    if type_ == 'flow':
        user_ = trigger_flow(user_, dialogue_flows, destination_id)

    if type_ == 'state':

        # If the user is not in the flow of the destination state
        if destination_id not in [state['id'] for state in flow_obj['states']]:
            # Find the id of the correct flow in which the state exists
            flow_id = find_flow_id(dialogue_flows, destination_id)
            # Trigger that flow first
            user_ = trigger_flow(user_, dialogue_flows, flow_id)

        user_ = trigger_state(user_, destination_id)

    return user_
