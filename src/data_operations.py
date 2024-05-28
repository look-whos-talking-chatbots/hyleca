"""
File that contains core data operation functions
"""


def inject_variable(data, var_path, variable):
    var_path = var_path.split('.')
    if len(var_path) == 1:
        vp = var_path[0]
        data[vp] = variable
    else:
        for i, vp in enumerate(var_path):

            if i == 0:
                value = data[vp]
            else:
                if len(var_path) - 1 == i:
                    value[vp] = variable
                else:
                    if vp in value:
                        value = value[vp]
                    else:
                        value[vp] = {}
                        value = value[vp]

    return data


def parse_variable(data, var_path):

    # Parse the variable path to retrieve the actual value from the data
    var_path = var_path.split('.')
    value = None
    for i, vp in enumerate(var_path):

        if i == 0:
            # the first value of the path should always be one of the default user fields
            value = data[vp]
        else:
            # If the next field already exists in the path just get its value
            if vp in value:
                value = value[vp]
            else:
                # if the next field does not exist,
                # and it is not the last field in the requested path
                # give an empty dictionary to the list, so it can add more to its path
                if i + 1 != len(var_path):
                    value = {}
                else:
                    # if the next field does not exist,
                    # and it is also the last field given in the path
                    # give None to it's value
                    value = None

    return value


def check_condition(data, condition):
    """Checks whether a given condition is true or false.

    :param dictionary data: Object contains the information that the conditions should be tested against.
    :param tuple condition: Tuple containing three variables; variable path, condition value, condition operator.
    :return bool flag: Boolean value that indicates whether condition is true or false.
    """
    flag = False

    var_path = condition[0]
    condition_value = condition[1]
    condition_operator = condition[2]

    value = parse_variable(data, var_path)

    # Parse the rule
    if ((condition_operator == '==' and value == condition_value)
            or (condition_operator == '!=' and value != condition_value)
            or (condition_operator == '>' and value is not None and value > condition_value)
            or (condition_operator == '<' and value is not None and value < condition_value)
            or (condition_operator == '>=' and value is not None and value >= condition_value)
            or (condition_operator == '<=' and value is not None and value <= condition_value)
            or (condition_operator == 'in' and condition_value in value)
            or (condition_operator == '!in' and condition_value not in value)):
        flag = True

    return flag


def are_conditions_met(user, conditions_list):
    """Simply checks if all conditions in the list are met and returns a boolean

    :param user:
    :param conditions_list:
    :return:
    """
    return all(check_condition(user, cond) for cond in conditions_list) or len(conditions_list) == 0
