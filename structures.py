"""
Functions to handle data structures (dictionaries, tuples or lists)"
"""
import pprint

####################################################################################################
# FUNCTIONS TO DESCRIBE LISTS AND DICTIONARIES
####################################################################################################

def print_dictdescription(input_dict, dictname = "dictionary", printinstructions = True):
    """
    Input: any dictionary
             printinstructions will let some intermediate stepts to be reported on-screen
    Objective: count the rows in the dictionary and print it.
    Returns: a string describing the dictionary.
    """
    dictdescription_string = "{0} rows found in {1}: \n{2}\n".format(len(input_dict), dictname, input_dict)
    if printinstructions == True: print(dictdescription_string)

    return dictdescription_string

####################################################################################################
# FUNCTIONS TO CONVERT STRING REPRESENTATIONS TO DATA STRUCTURES
####################################################################################################

def str_to_simplelist(string):
    """
    Input: string
    Output: list
    """
    string = string [1:-1].replace(" ", "").replace('"', "").replace("'", "")
    output_list = string.split(",")

    return output_list

####################################################################################################
# FUNCTIONS TO COMPARE LISTS AND DICTIONARIES
####################################################################################################

def getdictkeys(input_dict, name = "dictionary", printinstructions = True):
    """
    Input: any dictionary and its name (optional)
             printinstructions will let some intermediate stepts to be reported on-screen
    Objective: count the rows in the dictionary and print it.
    Returns: a list containing the dictionary keys.
    """

    # Get the dictionary keys
    dictvalues_list = [x for x in input_dict.keys()]
    if printinstructions == True:
        print("{0} keys found in {1}: \n{2}\n".format(
            len(dictvalues_list), name, dictvalues_list))

    return dictvalues_list

####################################################################################################

def compare_twolists(list1, list2, list1name = "", list2name = "", printinstructions = True):
    """
    Input: two dictionaries and their names (optional strings),
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: comparing two lists.
    Output: tuple of the form (are values the same?, which values are different).
    """

    # Get what is in list1 but not in list2
    list1_notin_list2 = [x for x in list1 if x not in list2]
    if printinstructions == True:
        print("{0} keys found in {2} but not in {3}: \n{1}\n".format(
            len(list1_notin_list2), list1_notin_list2, list1name, list2name))

    # Get what is in list2 but not in list1
    list2_notin_list1 = [x for x in list2 if x not in list1]
    if printinstructions == True:
        print("{0} keys found in {3} but not in {2}: \n{1}\n".format(
            len(list2_notin_list1), list2_notin_list1, list1name, list2name))

    if list1_notin_list2 == [] and list2_notin_list1 == []: same = True
    else: same = False

    return (same, list1_notin_list2, list2_notin_list1)

####################################################################################################

def compare_twodictkeys(dict1, dict2, dict1name = "", dict2name = "", printinstructions = True):
    """
    Input: two dictionaries and their names (optional strings),
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: comparing two dictionary keys.
    Output: tuple of the form (are values the same?, which values are different).
    """
    # Get lists with dictionary keys
    dict1keys = getdictkeys(dict1, dict1name, printinstructions)
    dict2keys = getdictkeys(dict2, dict2name, printinstructions)

    # Generate names for the dictionary key names to appear on screen
    if dict1name == "": dict1keysname = "dictionary keys"
    else: dict1keysname = dict1name + " keys"

    if dict2name == "": dict2keysname = "dictionary keys"
    else: dict2keysname = dict2name + " keys"

    dictkey_comparison = compare_twolists(dict1keys,
                                          dict2keys,
                                          dict1keysname,
                                          dict2keysname,
                                          printinstructions)

    dict1keys_notin_dict2keys = dictkey_comparison[1]
    dict2keys_notin_dict1keys = dictkey_comparison[2]

    # Get what is in one dictionary but not in the other
    dict1_notin_dict2 = {x : dict1[x] for x in dict1keys_notin_dict2keys}
    if printinstructions == True:
        print("{0} rows found in {1} but not in {2}:".format(
            len(dict1_notin_dict2), dict1name, dict2name))
        pprint.pprint(dict1_notin_dict2)
        print("")

    dict2_notin_dict1 = {x : dict2[x] for x in dict2keys_notin_dict1keys}
    if printinstructions == True:
        print("{0} rows found in {2} but not in {1}:".format(
            len(dict2_notin_dict1), dict1name, dict2name))
        pprint.pprint(dict2_notin_dict1)
        print("")

    if dict1_notin_dict2 == {} and dict2_notin_dict1 == {}: same = True
    else: same = False

    return (same, dict1_notin_dict2, dict2_notin_dict1)

####################################################################################################

def compare_twodictsfull(dict1, dict2, dict1name = "", dict2name = "", printinstructions = True):
    """
    Input: two dictionaries and their names (optional strings),
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: comparing two dictionaries in full.
    Output: tuple of the form  (rows in dict1 not in dict2,
                                rows in dict2 not in dict1,
                                rows in both which are different).
    """
    # This line will print a comparison between both
    key_comparison = compare_twodictkeys(dict1, dict2, dict1name, dict2name, printinstructions)
    # Keys in dict1 but not in dict2: key_comparison[1]
    # Keys in dict2 but not in dict1: key_comparison[2]

    # Get what is in both dictionaries in the keys present in both dictionaries
    union1 = {x : dict1[x] for x in dict1 if x not in key_comparison[1] }
    union2 = {x : dict2[x] for x in dict2 if x not in key_comparison[2] }

    # Show the discrepancies in tuples
    discrepancies = {x : (dict1[x], dict2[x]) for x in union1 if union1[x] != union2[x]}
    if printinstructions == True:
        if dict1 == "" and dict2 == "": autofill = " between both dictionaries"
        else: autofill = " between {0} and {1}".format(dict1name, dict2name)
        print("{0} discrepancies found{1}:".format(
            len(discrepancies), autofill))
        pprint.pprint(discrepancies)
        print("")

    return (key_comparison[1], key_comparison[2], discrepancies)

####################################################################################################
# FUNCTIONS TO MODIFY HOW DATA STRUCTURES ARE STRUCTURED
####################################################################################################

def dictlist_to_dictdict(input_dict, field = ""):
    """
    Input: nested data structure of the form dictionary → list
            if field is blank, the keys will be the rows
            if field is not blank, the keys will be one of the fields in the inner dictionary
    Objective: change inner lists into dictionaries.
    Output: nested data structure of the form dictionary → dictionary.
            The key in the middle dictionary is a string of the item index within the original list.
    """
    output_dict = {}

    input_dict_keys = list(input_dict.keys())

    if type(input_dict[input_dict_keys[0]]) is list:
        for key in input_dict_keys:
            # The same outer key will be kept but the item will be a dictionary instead of a list
            output_dict[key] = {}

            for row in input_dict[key]:
                # The new inner key will be the row index within the original list
                if field == "":
                    index = input_dict[key].index(row)
                    output_dict[key][index] = row
                # The new inner key will be one of the fields in the dictionaries within the list
                else:
                    index = row[field]
                    output_dict[key][index] = row

    else:
        print("""
    Item could not be converted from the form dictionary → list
                                  to the form dictionary → dictionary.
        """)
        output_dict = input_dict

    return output_dict

####################################################################################################

def flatten_dictdictdict(input_dict, additional_field = "original_key"):
    """
    Input:
        nested data structure of the form dictionary → dictionary → dictionary
        the name that will be
    Objective: the outermost dictionary key will be turned into a field in the innermost dictionary.
    Output: nested data structure of the form dictionary → dictionary, where
            the inner dictionary will have an additional field.
    """
    output_dict = {}

    # Add the outermost_key in the inner_dict again
    for outermost_key in input_dict:
        for outer_key in input_dict[outermost_key]:
            input_dict[outermost_key][outer_key][additional_field] = outermost_key

    # Populate the output_dict
    outermost_keys = list(input_dict.keys())
    for outermost_key in outermost_keys:
        for outer_key in input_dict[outermost_key]:
            if outermost_keys.index(outermost_key) > 0:
                # A new absolute key is created where the previous keys are counted
                try: # If the key is a number this will work
                    absolute_outer_key = outer_key + \
                                     len(input_dict[outermost_keys[outermost_keys.index(outermost_key) - 1]])
                except:
                    pass
            else: # If the key is text OR we are just starting (key = 0)
                absolute_outer_key = outer_key
            output_dict[absolute_outer_key] = input_dict[outermost_key][outer_key]

    return output_dict

####################################################################################################

def listlist_to_dictdict (input_list, fieldname_list = ""):
    """
    Inputs:
        A list containing lists with data and a list containing fieldnames (optional).
        If fieldname_list is blank, it will be assumed that the fieldnames are in row 0 of input_list.
    Output:
        Returns a nested dictionary where the outer dictionary index is the row in the original data list.
        The inner dictionaries match the cells in that row to the field names.
    """
    output_dict = {}

    if fieldname_list = "":
        fieldnames = input_list[0]
        data_list = input_list [1:]

    for row in data_list:  # Exclude the row with the field names
        if len(row) > 0: # Skip empty rows
            # Create an empty dictionary for each row
            row_dict = {}
            for fieldname in fieldnames:
                row_dict[fieldname] = row[fieldnames.index(fieldname)]
            idx = row_dict[keyfield]
            output_dict[idx] = row_dict

    return output_dict
