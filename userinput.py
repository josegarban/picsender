"""
Functions to obtain user input
"""
def choose_mode_populate ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """

    output_dict  = {}
    outputtype   = None

    print("""
This script will get datasheets and pictures from a folder to create or update a database with the personal information.
    """)

    # Select how search text will be sourced

    # Get folder name
    # if sourcetype == "folder":
    #     folder = ""
    #     print("Insert the folder absolute path. If it's the same folder as this script, hit ""Enter"".")
    #     folder = input("")
    #     output_dict ["sourcetype"] = (sourcetype, folder)

    # Output generation
    while outputtype not in ("1", "2"):
        print("\nHow should the output be produced?")
        print("1. Update current .sqlite database.")
        print("2. Create a fresh .sqlite database.")
        outputtype = input("Type your choice. ")

    if outputtype == "1":
        outputfile = "current.sqlite"
        outputname = input_filename()

    elif outputtype == "2":
        outputfile = "fresh.sqlite"
        outputname = "output"

    output_dict["outputtype"] = (outputfile, outputname)

    print("")

    return output_dict

####################################################################################################

def choose_mode_refine ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """
    mode = {}
    mode["listcolumn_name"]        = ""
    mode["additionalcolumn_names"] = ""
    mode["separator"]              = ""
    mode["pythonic"]               = ""
    mode["sql_filename"]           = ""
    mode["sql_parenttable"]        = ""
    mode["parentdbkey_column"]     = ""
    mode["sql_childtable"]         = ""
    mode["childfk_name"]           = ""
    mode["printinstructions"]      = ""

    while mode["listcolumn_name"]        == "":
        print("\nWhat is the name of the column containing a list representation?")
        mode["listcolumn_name"]        = input("")
    
    while mode["additionalcolumn_names"] == "":
        print("\nShould other columns be copied into the new table?")
        print("\nInsert their names separated by commas.")
        mode["additionalcolumn_names"] = input("").rstrip().split(",")
    
    while mode["separator"]              == "":    
        print("\nWhat is the separator character between the columns?")
        mode["separator"]              = input("")
    
    while mode["printinstructions"] not in ("True", "False"):
        print("\nDoes the list start with '[' and end in ']'?")
        mode["pythonic"]               = input("")
        if mode["pythonic"] == "True": mode["pythonic"] = True
        elif mode["pythonic"] == "False": mode["pythonic"] = False
        
    while mode["sql_filename"]           == "":
        print("\nWhat is the name of the sql file?")
        mode["sql_filename"]           = input("")
        
    while mode["sql_parenttable"]        == "":
        print("\nWhat is the name of the sql parent table?")
        mode["sql_parenttable"]        = input("")
    
    while mode["parentdbkey_column"]     == "":
        print("\nWhat is the name of the parent table key column?")
        mode["parentdbkey_column"]     = input("")
    
    while mode["sql_childtable"]         == "":
        print("\nWhat is name of the new child table?")
        mode["sql_childtable"]         = input("")
    
    while mode["childfk_name"]           == "":
        print("\nWhat is the name of the foreign key to relate child and parent tables?")
        mode["childfk_name"]           = input("")

    while mode["printinstructions"] not in ("True", "False"):
        print("\nShould intermediate steps be printed? True/False")
        mode["printinstructions"]      = input("")
        if mode["printinstructions"] == "True": mode["printinstructions"] = True
        elif mode["printinstructions"] == "False": mode["printinstructions"] = False

    return mode
    
####################################################################################################

def input_filename():
    """
    Input: typed by user.
    Objective: get a filename for other functions to use.
    Output: string.
    """
    output_string = ""

    while output_string == "":
        print("Please type the filename or path. Don't forget to add the extension at the end.")
        output_string = input("")

    return output_string
