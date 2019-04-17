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
    Input: string with a pythonic representation of a list.
    Objective: converts a string representation of a list into a list. 
    Output: list
    """
    string = string [1:-1].replace(" ", "").replace('"', "").replace("'", "")
    output_list = string.split(",")

    return output_list

def strspaces_to_simplelist(input_string, separator = " "):
    """
    Input: a string and a separator (optional).
    Objective: converts a string representation of a list into a list. Can be used for non-pythonic list representations.
    Output: a list.
    """
    
    if separator not in input_string: return [input_string]
    else:
        output_list = list(input_string.split(separator))
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

def listlist_to_dictdict (input_list, fieldname_list = "", keyfield = "id"):
    """
    Inputs:
        A list containing lists with data and a list containing fieldnames (optional).
        If fieldname_list is blank, it will be assumed that the fieldnames are in row 0 of input_list.
        The keyfield name that will become the primary key, called 'id' by default.
    Output:
        Returns a nested dictionary where the outer dictionary index is the row in the original data list.
        The inner dictionaries match the cells in that row to the field names.
    """
    output_dict = {}

    if fieldname_list == "":
        fieldnames = input_list[0]
        data_list  = input_list[1:]
    else:
        fieldnames = fieldname_list
        if input_list[0] == fieldname_list:
            data_list  = input_list[1:]
        else:
            data_list  = input_list

    for row in data_list:  # Exclude the row with the field names
        if len(row) > 0: # Skip empty rows
            # Create an empty dictionary for each row
            row_dict = {}
            for fieldname in fieldnames:
                row_dict[fieldname] = row[fieldnames.index(fieldname)]
                # Create an id field if it does not exist, else use the field set by the user
                if keyfield == "id" and "id" not in fieldnames: idx = data_list.index(row)
                else: idx = row_dict[keyfield]
            output_dict[idx] = row_dict

    return output_dict


####################################################################################################
# FUNCTIONS TO ABRIDGE DATA STRUCTURES 
####################################################################################################

def tuplist_sieve(tup_list, wantedtup_list = "", position = 0):
    """
    Input: a list consisting of tuples,
            a list to define which values are wanted in the tuples that will remain
            a position where the values are found, default is 0
    Objective: filter a tup_list consisting of several tuples provided that the values within them are
            in wantedtup_list in the position position.
    Output: a list consisting of tuples.
    """
    output_list = []
    if wantedtup_list == "": wantedtup_list = tup_list # If wantedtup_list is empty, output = input
    
    for tup in tup_list:
        if tup[position] in wantedtup_list:
            output_list.append(tup)

    return output_list

####################################################################################################

def keep_members_inlist(input_list, input_choice = ""):
    """
    Input: a list with several items.
            predetermined choice, that can be left blank to prompt the user for an answer.
    Output: a list with the items to be kept.
    """
    print("The input list consists of the following elements: ")
    tuples = [(input_list.index(element), element) for element in input_list]
    print(input_list)
    
    if input_choice == "":
        print("\nWhich do you want to keep? Type the relevant indices separated by commas.")
        choice = input("")
        # Get indices as integers
        try:
            chosen_indices = [int(x) for x in list(choice.replace(" ,",",").replace(", ",",").split(","))]
            output_list = [x[1] for x in tuples if x[0] in chosen_indices]
        except:
            print("The input may not have consisted of integers. No changes will be made to the original list. Try again.")
            return input_list

    else:
        print("\nThe following elements will be kept, if applicable:", input_choice)
        output_list = [x for x in input_list if x in input_choice] # Nothing has to be converted to numbers
    
    if len(output_list) == 0:
        print("The abridged list is empty. Possibly your desired elements are not in the original list:")
        print(output_list)
    else:
        print("The abridged list contains the following members:")
        print(output_list, "")
    
    return output_list


####################################################################################################
# FUNCTIONS TO EXPAND DATA STRUCTURES 
####################################################################################################

def expand_dict (input_dict, listcolumn_name, oldkey):
    """
    Input: dictionary,
            fieldname consisting of lists or tuples,
            name of the key column in output_dict[newkey][?] into which the old key will be copied.
            
    Objective: if there is a column whose values are lists, the records in the dictionary will be multiplied.
    Output: dictionary
    """
    output_dict = {}
    keys = list(input_dict.keys())
    
    # If parent_dict is a nested dictionary
    if type(input_dict[keys[0]]) is dict:
        length_i = 0 # Counter up to the length of the input dictionary
        length_o = 0 # Counter up to the length of the output dictionary
        while length_i < len(keys):
            length_o += len(input_dict[keys[length_i]][listcolumn_name])
            length_i += 1
        
        for i in list(range(len(keys))):
            outer_key = keys[i]                            
            # Length of the list to be expanded
            for k in list(range(len(input_dict[outer_key][listcolumn_name]))): 
                member_row = {}
                for inner_key in input_dict[outer_key]:
                    member_row[inner_key] = input_dict[outer_key][inner_key]
        
                # The list is replaced by an element within it
                member_row[listcolumn_name] = input_dict[outer_key][listcolumn_name][k]
                # The old key is moved to within the dictionary row
                member_row[oldkey]          = outer_key
                # The output_dict will have keys consisting of the old outer_key + list element
                output_dict[2*i+k]       = member_row
                print(2*i+k, k, i, member_row)
            
    print("\n"*5, output_dict)

    return output_dict