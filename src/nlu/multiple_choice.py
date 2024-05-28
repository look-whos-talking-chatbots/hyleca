"""
Contains the functions to execute states with multiple choice questions
"""

from src.data_operations import inject_variable


def multiple_choice(user, state_obj, user_input):
    user_input = user_input.lower().split()

    choice = None

    if 'multipleChoice' in state_obj and state_obj['multipleChoice']:

        multi_cho = state_obj['multipleChoice']

        letters = multi_cho[0].split(',')
        variables = multi_cho[0].split(',')
        var_path = multi_cho[1]

        if len(multi_cho) == 3:
            letters = multi_cho[0].split(',')
            variables = multi_cho[1].split(',')
            var_path = multi_cho[2]

        try:
            for i, let in enumerate(letters):
                if let in user_input:
                    choice = variables[i]
        except:
            choice = None

        user = inject_variable(user, var_path, choice)

    return user
