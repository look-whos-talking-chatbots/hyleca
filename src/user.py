"""
File that contains functions for operations purely on user data
"""

from datetime import datetime

from src.state_handler import get_current_flow, get_candidate_states


def init_user(bot, incoming_data):

    creation_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Default user data
    user = {
        "id": incoming_data['user_id'],
        "user_name": incoming_data['user_name'],
        "bot": {
            "token": incoming_data['token'],
            "name": bot.name,
            "version": bot.version,
            "language": bot.language
        },
        "name": None,
        "age": None,
        "params": {},
        "temporary": {},
        "progress": {
            "flow": {
                "past": [],
                "current": -1,
            },
            "state": {
                "past": [],
                "current": -1,
                "exchangeCounter": 0,
                "question": {
                    "isNext": True,
                    "isAsked": False
                },
                "response": {
                    "wasGenerated": False,
                    "humanUtterance": {},
                    "counter": 0,
                }
            },
            "onhold": {
                "start": None,
                "duration": bot.onhold_duration if hasattr(bot, 'onhold_duration') else 1,
                "is": False
            }
        },
        "created_at": creation_time,
        "last_updated_at": creation_time,
    }

    # Initiate the user's current flow and state
    user['progress']['flow']['current'] = [f['id'] for f in bot.dialogue_flows][0]
    flow_obj = get_current_flow(user, bot.dialogue_flows)
    user['progress']['state']['current'] = get_candidate_states(flow_obj, user)[0]

    return user
