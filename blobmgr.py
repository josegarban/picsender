import sqlite3 as sqlite
import os.path
from filegenerator import files_in_folder_byext, generate_timestamp, string_to_txt
from dbhandler import get_alldbrows
from userinput import input_path

####################################################################################################

def add_blobtable(sql_filename = "",
                  blobtable = "blobtable",
                  printinstructions = True):
    """
    Inputs: filename,
            name of the table that will be updated or created.
            The table won't be created if it already exists.
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: create an empty table for blobs.
    Outputs: none.
    """
    output_string = generate_timestamp() + "\n"*2
    
    # Open the database and get the table name if none has been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if blobtable == "": blobtable = input("Insert table name:")
    
    my_connector = sqlite.connect(sql_filename)
    my_cursor    = my_connector.cursor()
    
    if not os.path.exists(sql_filename): print("File {0} does not exist.\n".format(sql_filename))
    
    else:
        # Build the instruction to be executed to create the table 
        instruction = """CREATE TABLE IF NOT EXISTS Blobtable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data BLOB,
        type TEXT,
        filename TEXT,
        filepath TEXT,
        searchterm TEXT);"""
        
        #Create the table
        my_cursor.execute(instruction)
        if printinstructions == True: print("Instruction executed:", instruction)
        output_string = output_string + instruction + "\n"
        
    # Commit the changes
    my_connector.commit()
    my_connector.close()
    
    # Generate report
    output_filename = sql_filename + "_history.txt"
    string_to_txt(output_filename, output_string)
    
    return None

####################################################################################################

def insert_blob(blob_file,
                sql_filename = "",
                blobtable = "blobtable",
                printinstructions = True):
    """
    Input: blob filename,
            .sqlite where the file will be saved,
            table where the file will be saved,
            printinstructions will let some intermediate steps to be reported on-screen.
    Objective: insert a blob file into a .sqlite file table.
    Output: None
    """
    output_string = generate_timestamp() + "\n"*2
    
    # Open the database and get the table name if none has been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if blobtable == "": blobtable = input("Insert table name:")
    
    my_connector = sqlite.connect(sql_filename)
    my_cursor    = my_connector.cursor()
    if not os.path.exists(sql_filename): print("File {0} does not exist.\n".format(sql_filename))
    
    else:
        with open(blob_file, 'rb') as file:
            ablob = file.read()
            base = os.path.basename(blob_file)
            afile, ext = os.path.splitext(base)
            instruction = """INSERT INTO {0} (data, type, filename, filepath) VALUES(?, ?, ?, ?);""".format(blobtable)
            
            my_cursor.execute(instruction, (sqlite.Binary(ablob), ext, afile, base+afile+ext))
            if printinstructions == True: print("Instruction executed:", instruction)
            output_string = output_string + instruction + string(values) + "\n"
    
    # Commit the changes
    my_connector.commit()
    my_connector.close()
    
    # Generate report
    output_filename = sql_filename + "_history.txt"
    string_to_txt(output_filename, output_string)

    return None

####################################################################################################

def insert_blobs(extensions,
                 folder = "",
                 sql_filename = "",
                 blobtable = "blobtable",
                 printinstructions = True):
    """
    Input: list of valid extensions,
            blob path where the blob files are found (if left empty the same path will be used),
            .sqlite where the file will be saved,
            table where the file will be saved,
            printinstructions will let some intermediate steps to be reported on-screen.
    Objective: insert several blob files into a .sqlite file table.
    Output: None
    """
    # Open the database and get the table name if none has been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if blobtable == "": blobtable = input("Insert table name:")
    if folder == "": folder = input_path()
        
    if not folder.endswith("\\"): folder = folder + "\\"
    
    my_files = files_in_folder_byext (folder, extensions)
    
    for file in my_files:
        insert_blob(folder+file,
                    sql_filename,
                    blobtable,
                    printinstructions)
        
    
####################################################################################################

def insert_searchterm(criteria = "endswith",
                      parameter = 3,
                      sql_filename = "",
                      blobtable = "blobtable",
                      dbkey_column = "id",
                      printinstructions = True):
    """
    Input:  first or last characters?
            how many?
            blob filename,
            .sqlite file where the data is saved,
            table where the data is saved,
            name of the key column in the blob table
            printinstructions will let some intermediate steps to be reported on-screen.
    Objective: insert a searchterm of the first or last x characters.
    Output: None
    """
    output_string = generate_timestamp() + "\n"*2

    # Open the database and get the table name if none has been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if blobtable == "": blobtable = input("Insert table name:")
    
    my_connector = sqlite.connect(sql_filename)
    my_cursor    = my_connector.cursor()
    if not os.path.exists(sql_filename): print("File {0} does not exist.\n".format(sql_filename))
    
    else:
        input_dict = get_alldbrows(sql_filename,
                                   blobtable,
                                   dbkey_column,
                                   False)

        for row in input_dict:
            filename = input_dict[row]["filename"]
            if   criteria == "endswith":   values = (filename[-parameter:] , filename)
            elif criteria == "startswith": values = (filename[:parameter-1], filename)
        
            instruction = """UPDATE {0} SET searchterm = ? WHERE filename = ?;""".format(blobtable)
            output_string = output_string + instruction + string(values) "\n"
            my_cursor.execute(instruction, values)
            if printinstructions == True: print("Instruction executed:", instruction, values)
    
    # Commit the changes
    my_connector.commit()
    my_connector.close()
    
    # Generate report
    output_filename = sql_filename + "_history.txt"
    string_to_txt(output_filename, output_string)
    
    return None
    