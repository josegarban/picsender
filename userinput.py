import dbhandler
import os

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
    mode["blobfolder"]             = ""
    mode["searchdirection"]        = ""
    mode["searchchars"]            = 0
    mode["saveblobs"]              = None

    if sql_filename == "":
        mode["sql_filename"] = ""
        while mode["sql_filename"] == "":
            print("\nWhat is the name of the sql file? Please include the extension at the end. Leave input blank for default: 'output.sqlite'")
            mode["sql_filename"] = input("")
            if mode["sql_filename"] == "":
                mode["sql_filename"] = "output.sqlite"
        while not os.path.exists(mode["sql_filename"]):
            print("\nThis file was not found. Try again.")
            mode["sql_filename"] = input("")

    while mode["sql_parenttable"] == "":
        print("\nWhat is the name of the sql parent table? Leave input blank for default: 'rawdata'.")
        mode["sql_parenttable"] = input("")
        if mode["sql_parenttable"] == "":
            mode["sql_parenttable"] = 'rawdata'

    while mode["parentdbkey_column"] == "":
        print("\nWhat is the name of the parent table key column? Leave input blank for default: 'id'")
        mode["parentdbkey_column"] = input("")
        if(mode["parentdbkey_column"]) == "":
            mode["parentdbkey_column"] = "id"

    columns = dbhandler.get_alldbcolumns(mode["sql_filename"],
                                 mode["sql_parenttable"],
                                 mode["parentdbkey_column"],
                                 False)
    print("\nThe columns in table {0} in file {1} are:".format(mode["sql_parenttable"], mode["sql_filename"]))
    print(columns)

    while mode["listcolumn_name"] == "":
        print("\nWhat is the name of the column containing a list representation?")
        mode["listcolumn_name"] = input("")

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

    while mode["separator"] == "":
        print("\nWhat is the separator character between the columns?")
        mode["separator"] = input("")

    while mode["pythonic"] is None:
        print("\nDoes the list start with '[' and end in ']'? Y/N")
        mode["pythonic"] = input("")
        if mode["pythonic"] in ("Y", "y"):
            mode["pythonic"] = True
            pass
        elif mode["pythonic"] in ("N", "n"):
            mode["pythonic"] = False
            pass
        else:
            print("Incorrect input, please start again.")
            quit()

    while mode["sql_childtable"] == "":
        print("\nWhat is the name of the new child table? Default name: 'child'.")
        mode["sql_childtable"] = input("")

        mode["childfk_name"] = mode["sql_parenttable"] + mode["parentdbkey_column"]

    while mode["printinstructions"] is None:
        print("\nShould intermediate steps be printed? Y/N")
        mode["printinstructions"] = input("")
        if mode["printinstructions"] in ("Y", "y"):
            mode["printinstructions"] = True
            pass
        elif mode["printinstructions"] in ("N", "n"):
            mode["printinstructions"] = False
            pass
        else:
            print("Incorrect input, please start again.")
            quit()

    while mode["blobfolder"] == "":
        print("\nIn which folder are the attachments stored?")
        mode["blobfolder"] = input("")
        while not os.path.exists(mode["blobfolder"]):
            print("\nThis folder was not found. Try again.")
            mode["blobfolder"] = input("")

    while mode["saveblobs"] is None:
        print("\nShould attachments be integrally copied? Y/N")
        print("\nIf the attachments are large, copying them may take a while...")
        mode["saveblobs"] = input("")
        if mode["saveblobs"] in ("Y", "y"):
            mode["saveblobs"] = True
            pass
        elif mode["saveblobs"] in ("N", "n"):
            mode["saveblobs"] = False
            pass
        else:
            print("Incorrect input, please start again.")
            quit()

    while mode["searchdirection"] not in ("1", "2"):
        print("\nWill the file name search be conducted (1) from the beginning or (2) from the end of the file names?")
        print("Default: 2.")
        mode["searchdirection"] = input("Choose 1 or 2: ")
    if mode["searchdirection"] == "1": mode["searchdirection"] = "startswith"
    elif mode["searchdirection"] == "2": mode["searchdirection"] = "endswith"
    else: mode["searchdirection"] = "endswith"

    while mode["searchchars"] == 0:
        print("\nHow many characters will be matched during the search?")
        try:
            temp = input("")
            mode["searchchars"] = int(temp)
        except Exception:
            print("Incorrect input, please try again.")


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

####################################################################################################

def input_path():
    """
    Input: typed by user.
    Objective: get a folder path.
    Output: string.
    """
    output_string = ""

    while output_string == "":
        print("Please type the full path.")
        output_string = input("")

    return output_string
