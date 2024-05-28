"""
Script for interactively testing the talk functionality of the chatbots.

It helps to simulate an ongoing continuous conversation with a selected bot. The conversation history and the user data
is updated and saved to files, respectively called "last_history_<bot-token>.json" and "last_user_<bot-token>.json".
If you wish to reset the conversation and start over, you can remove or rename these two files. This would force the
script to create two new files from scratch which would have no data on the history or the user.

NOTE: A bot token is a unique identifier that helps to system the load the correct bot.
      Each bot should be registered to the AGENT_INDEX in the __init__.py file in its own folder.
      AGENT_INDEX object contains unique bot tokens as its keys.
"""
import sys
import time
import json
import traceback
from copy import deepcopy
from datetime import datetime

from settings import PROJECT_PATH

sys.path.append(PROJECT_PATH)

from src.agents import get_bot
from src.talk import talk
from src.user import init_user


def save_records(user_file_, history_file_):
    with open(user_file_, 'w') as jf_u:
        json.dump(USER, jf_u)
    with open(history_file_, 'w') as jf_h:
        json.dump(HISTORY, jf_h)


# WARNING: You have to give a token of a bot for this script to function.
# (e.g. "example-bot" or "example-bot-generative")
BOT_TOKEN = 'example-bot'

if __name__ == "__main__":

    MAX_CHAT_HISTORY_SIZE = 5

    # Imitation of the data sent by Rocket.Chat outgoing webhooks.
    INCOMING_DATA_ = {
        'text': '',
        'token': BOT_TOKEN,
        'bot': False,
        'user_name': 'TEST-USER',
        'user_id': 'TEST-USER-ID',
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    user_file = f"{PROJECT_PATH}/tests/last_user_{INCOMING_DATA_['token']}.json"
    history_file = f"{PROJECT_PATH}/tests/last_history_{INCOMING_DATA_['token']}.json"

    try:
        with open(user_file, 'r') as jf:
            USER = json.load(jf)
    except OSError:
        USER = None

    try:
        with open(history_file, 'r') as jf:
            HISTORY = json.load(jf)
    except OSError:
        HISTORY = []

    # Note: If you wish to jump to a custom state activate the next lines.
    #       Beware that the USER may not have the required data to run the particular state
    #       It is advised to do this with a full USER data.
    # USER['progress']['flow']['current'] = 1111
    # USER['progress']['state']['current'] = 1004

    if USER:
        print("\nCurrent flow and state: ",
              USER['progress']['flow']['current'], '-',
              USER['progress']['state']['current'], '\n')

    if HISTORY:
        print('Here is a recap of the conversation so far:')
        for utterance in HISTORY[-MAX_CHAT_HISTORY_SIZE:]:
            agent = '- BOT: ' if utterance['bot'] else '- USER:'
            text = deepcopy(utterance['text'])
            text = text.replace('\n', '\n        ')
            print(agent, text)

    try:
        while True:

            input_text = input("\n>> Me:  ")

            incoming_data = deepcopy(INCOMING_DATA_)
            incoming_data['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            incoming_data['text'] = input_text

            bot = get_bot(incoming_data['token'])

            if not USER:
                USER = init_user(bot, incoming_data)

            # Enrich incoming data based on users last recorded data
            incoming_data['flow_id'] = USER['progress']['flow']['current']
            incoming_data['state_id'] = USER['progress']['state']['current']
            # Enrich the incoming data with bot info
            incoming_data['bot_info'] = {
                'name': bot.name,
                'version': bot.version,
            }

            # Push data to "database"
            HISTORY.append(incoming_data)

            user_input = incoming_data['text']

            # WARNING: The following filters out the generated text from the history before moving on.
            chat_history = [h for h in HISTORY
                            if ('generator' not in h
                                or ('generator' in h and h['generator']))]

            # NOTE: MAX_CHAT_HISTORY_SIZE refers to how many USER utterances should be in the history.
            #       Multiplication by 3 roughly accounts for the bot utterances.

            chat_history = chat_history[-MAX_CHAT_HISTORY_SIZE * 3:]

            outputs, USER, trigger_next_state = talk(USER, bot, user_input, history=chat_history)

            # NOTE: If there was a trigger to trigger a new state;
            #       call the talk() again, so the utterance from the new state is included.
            while trigger_next_state:
                new_outputs, USER, trigger_next_state = talk(USER, bot, user_input, history=chat_history)
                outputs += new_outputs

            if outputs:

                for output in outputs:

                    if len(output['text']) > 0:

                        interval = len(output['text']) / 400
                        # Prevent too short intervals
                        interval = interval if interval > 1 else 1
                        # Prevent too long intervals
                        interval = interval if interval < 3 else 3

                        time.sleep(interval)

                        output['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                        output['user_name'] = incoming_data['user_name']
                        output['bot'] = True
                        output['token'] = incoming_data['token']
                        output['bot_info'] = {
                            'name': bot.name,
                            'version': bot.version,
                        }

                        if 'trigger' in output:
                            del output['trigger']

                        # Push data to "database"
                        HISTORY.append(output)

                        print(f"[{str(output['state_id'])}]", "-",
                              output['text'],
                              f"({output['generator']})")

            else:
                # save_records(user_file, history_file)
                print('Bot has nothing to say. Ending the conversation')
                # break

    except KeyboardInterrupt:
        save_records(user_file, history_file)
        print('######################### INTERRUPTED #########################')

    except Exception:
        save_records(user_file, history_file)
        print('######################### ERROR #########################')
        print(traceback.print_exc())
