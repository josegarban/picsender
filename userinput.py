import dbhandler 

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

def choose_mode_refine (sql_filename = ""):
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """
    mode = {}
    mode["listcolumn_name"]        = ""
    mode["additionalcolumn_names"] = None
    mode["separator"]              = ""
    mode["pythonic"]               = None
    mode["sql_parenttable"]        = ""
    mode["parentdbkey_column"]     = ""
    mode["sql_childtable"]         = ""
    mode["childfk_name"]           = ""
    mode["printinstructions"]      = None

    if sql_filename == "":
        mode["sql_filename"] = ""
        while mode["sql_filename"]           == "":
            print("\nWhat is the name of the sql file? Please include the extension at the end.")
            mode["sql_filename"]           = input("")
        
    while mode["sql_parenttable"]        == "":
        print("\nWhat is the name of the sql parent table?")
        mode["sql_parenttable"]        = input("")
    
    while mode["parentdbkey_column"]     == "":
        print("\nWhat is the name of the parent table key column?")
        mode["parentdbkey_column"]     = input("")

    columns = dbhandler.get_alldbcolumns(mode["sql_filename"],
                                 mode["sql_parenttable"],
                                 mode["parentdbkey_column"],
                                 False)
    print("\nThe columns in table {0} in file {1} are:".format(mode["sql_parenttable"], mode["sql_filename"]))
    print(columns)
    
    while mode["listcolumn_name"]        == "":
        print("\nWhat is the name of the column containing a list representation?")
        mode["listcolumn_name"]        = input("")
    
    while mode["additionalcolumn_names"] == None:    
        print("\nShould other columns be copied into the new table?")
        print("Insert their names separated by commas or leave the input empty to include all columns.")
        additionalcolumns = input("")
        
        if additionalcolumns == "":
            mode["additionalcolumn_names"] = columns
        else:
            try:
                mode["additionalcolumn_names"] = list(additionalcolumns.rstrip().split(","))
            except Exception:
                print("Incorrect input, please start again.")
                quit()
    
    while mode["separator"]              == "":    
        print("\nWhat is the separator character between the columns?")
        mode["separator"]              = input("")
    
    while mode["pythonic"] is None:
        print("\nDoes the list start with '[' and end in ']'? True/False")
        mode["pythonic"]               = input("")
        if mode["pythonic"] == "True":
            mode["pythonic"] = True
            pass
        elif mode["pythonic"] == "False":
            mode["pythonic"] = False
            pass
        else:
            print("Incorrect input, please start again.")
            quit()
        
    while mode["sql_childtable"]         == "":
        print("\nWhat is name of the new child table?")
        mode["sql_childtable"]         = input("")
    
        mode["childfk_name"]           = mode["sql_parenttable"] + mode["parentdbkey_column"] 


    while mode["printinstructions"] is None:
        print("\nShould intermediate steps be printed? True/False")
        mode["printinstructions"]      = input("")
        if mode["printinstructions"] == "True":
            mode["printinstructions"] = True
            pass
        elif mode["printinstructions"] == "False":
            mode["printinstructions"] = False
            pass
        else:
            print("Incorrect input, please start again.")
            quit()

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
