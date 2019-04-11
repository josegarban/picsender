import filegenerator

"""
Functions to obtain user input
"""
def choose_primary_mode ():
    """
    Input: User input.
    Objective: Let the user choose which mode is to be used.
    Output: Dictionary containing the search parameters.
    """

    output_dict  = {}
    sourcetype   = None
    outputtype   = None

    print("""
This script will get datasheets and pictures from a folder to create or update a database with the personal information.
    """)

    # Select how search text will be sourced

    # Get folder name
    if sourcetype == "folder":
        folder = ""
        print("Insert the folder absolute path. If it's the same folder as this script, hit ""Enter"".")
        folder = input("")
        output_dict ["sourcetype"] = (sourcetype, folder)

    # Output generation
    while outputtype not in ("1", "2"):
        print("\nHow should the output be produced?")
        print("1. Update current .sqlite database.")
        print("2. Create a fresh .sqlite database.")
        outputtype = input("Type your choice. ")

    if outputtype == "1":
        outputfile = "current.sqlite"
        print("Insert filename or path without the .sqlite extension")
        outputname = input_filename()

    elif outputtype == "2":
        outputfile = "fresh.sqlite"
        outputname = "output"

    output_dict["outputtype"] = (outputfile, outputname)

    print("")

    return output_dict

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
