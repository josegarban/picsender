import pprint
import os

import time
import datetime

"""
Objective: create or read files
"""
####################################################################################################
# FILESYSTEM
####################################################################################################

def generate_timestamp ():
    """
    Inputs: None
    Returns: String with a timestamp to be appended to a file name
    """
    now = datetime.datetime.now()
    timestamp = now.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S")

    return timestamp

def generate_longtimestamp ():
    """
    Inputs: None
    Returns: String with a fully precise timestamp to be appended to a file name
    """
    now = datetime.datetime.now()
    timestamp = str(now.fromtimestamp(time.time())).replace(":", "").replace("-", "").replace(".", ",")

    return timestamp

####################################################################################################

def files_in_folder_byext (folder, extensions = ""):
    """
    Input: folder path, list of valid extensions (optional)
    Objective: find files of certain extensions in the same folder
    Output: list with filenames
    """
    
    if folder == "":
        # Find file(s) in same folder
        files = os.listdir()
    else:
        # Find file(s) in other folder
        files = os.listdir(folder)

    # Get a list with just html file names
    output_list  = []
    
    if extensions != "":
        for extension in extensions:
            for file in files: 
                if   file.endswith(extension): output_list.append(file)
        if len (output_list) == 0:
            print("No file with the searched extensions were found.")
            print("")
        else:
            print("The following files with the searched extensions were found:")
            pprint.pprint(output_list)
            print("")
    else:
        for file in files: 
            output_list.append(file)
        if len (output_list) == 0:
            print("No files were found.")
            print("")
        else:
            print("The following files were found:")
            pprint.pprint(output_list)
            print("")


    return output_list

####################################################################################################
# READ FILES
####################################################################################################

def txt_to_string(filename, strip=False):
    """
    Input: txt filename
    Output: list
    """
    output_string = ""
    print("  Reading file {0}...".format(filename))
    
    with open(filename, "r") as my_file:
        for line in my_file:
            if strip == True: line = line.rstrip()
            if strip == False: line = line
            output_string = output_string + str(line)

    return output_string

####################################################################################################
def txt_to_list(filename):
    """
    Input: txt filename
    Output: list
    """
    output_list = []
    print("  Reading file {0}...".format(filename))
    
    with open(filename, "r") as my_file:
        for line in my_file:
            line = line.rstrip()
            output_list.append(str(line))
            print("    Line {0}: {1}".format(output_list.index(line), line), "")

    if len(output_list) == 0: output_list = [""] # In case the file is empty we want a list, not a set
    return output_list

####################################################################################################

def file_to_string (filename):
    """
        Input: filename
        Objective: open a file and return a string, to be handled in-memory
        Output: string 
    """
    output_string = ""
    
    try:
        with open(filename, "r", errors="replace") as myfile:
            print("    Successfully opened {0}.".format(filename))
            for line in myfile:
                try:
                    line = line.rstrip()
                    line = line.encode('latin-1').decode('unicode-escape').encode('latin-1').decode('utf-8')
                    output_string = output_string + line
                except:
                    #print("Failed line", line)
                    pass

    except:
        print("\n    Failed to open {0}.\n".format(filename))
    print("output", output_string)        
    return output_string  

####################################################################################################
# OTHER FILETYPES MANIPULATION
####################################################################################################

def string_to_txt(filename, string):
    """
    Inputs: output filename, string.
    Objective: converts a string to a text file.
    Outputs: none.
    """
    
    text_file = open(filename, "a")
    text_file.write(string)
    text_file.write("\n"*2)
    text_file.close()
    
    return None