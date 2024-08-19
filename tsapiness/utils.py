# utils.py
from typing import Callable, List, Dict, Any


def add(d, label, obj, apply_to_tsapi=False):
    """
    Adds an object to a dictionary under a specified label.

    Args:
        d (dict): The dictionary to add the object to.
        label (str): The key under which the object will be added.
        obj (Any): The object to add to the dictionary.
        apply_to_tsapi (bool, optional): If True, calls the `to_tsapi`
        method on the object before adding it. Defaults to False.

    Returns:
        dict: The updated dictionary.
    """
    if apply_to_tsapi:
        if obj is not None:
            d[label] = obj.to_tsapi()
        return d
    else:
        if obj is not None:
            d[label] = obj
        return d


def parse(list_to_parse: List[Dict[str, Any]],
          obj: Callable[..., Any]) -> List[Any]:
    """
    Parses a list of dictionaries into a list of objects.

    Args:
        list_to_parse (List[Dict[str, Any]]): The list of dictionaries to
        parse.
        obj (Callable[..., Any]): The callable (usually a class) to
        instantiate with each dictionary.

    Returns:
        List[Any]: A list of instantiated objects.
    """
    list_to_return = []
    if list_to_parse is not None:
        for list_item in list_to_parse:
            list_item_obj = obj(**list_item)
            list_to_return.append(list_item_obj)
    return list_to_return


def flatten_variable(variable, variable_list):
    """
    Recursively flattens a variable and its nested variables into a list of
    dictionaries.

    Args:
        variable (Variable): The variable to flatten.
        variable_list (list): The list to append the flattened variables to.

    Returns:
        list: The list of flattened variables as dictionaries.
    """
    if len(variable.looped_variables) > 0 and len(variable.values) > 0:
        # If the variable has both looped variables and values, flatten both.
        for value in variable.values:
            _a = variable.to_dict()
            _a.update(value.to_dict())
            variable_list.append(_a)
        for loop_variable in variable.looped_variable_values:
            flatten_variable(variable=loop_variable,
                             variable_list=variable_list)
    elif len(variable.looped_variables) == 0 and len(variable.values) > 0:
        # If the variable has values but no looped variables,
        # flatten the values.
        _a = variable.to_dict()
        for value in variable.values:
            _a = variable.to_dict()
            _a.update(value.to_dict())
            variable_list.append(_a)
    elif len(variable.looped_variables) > 0 and len(variable.values) == 0:
        # If the variable has looped variables but no values, do nothing.
        pass
    elif len(variable.looped_variables) == 0 and len(variable.values) == 0:
        # If the variable has neither looped variables nor values, just add it.
        _a = variable.to_dict()
        variable_list.append(_a)
    else:
        # Default case: add the variable as is.
        _a = variable.to_dict()
        variable_list.append(_a)

    if len(variable.otherSpecifyVariables) > 0:
        # If the variable has other specify variables, flatten them as well.
        for osv in variable.otherSpecifyVariables:
            flatten_variable(variable=osv, variable_list=variable_list)

    return variable_list
