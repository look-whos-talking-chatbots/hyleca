"""
File contains the common text classification functions for chatbots.

The functions under this file should always expect "user_input" and "language" as their input.
They should always return a single variable, but the type of the variable can be integer, string, boolean, and None
depending on your application.
"""


def categorize_placeholder(user_input, language):
    """Useful during chatbot development"""
    return user_input


def categorize_yes_no(user_input, language):
    """Dummy function to recognize whether user said yes or no"""
    user_input = user_input.lower().split()
    if any(word in user_input for word in ['yes', 'ys', 'y', 'yees', 'yeees', 'yeap', 'yeah', 'ok']):
        return 'yes'
    elif any(word in user_input for word in ['no', 'n', 'noo', 'noooo']):
        return 'no'
    else:
        return None
