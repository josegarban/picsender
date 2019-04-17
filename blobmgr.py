import sqlite3 as sqlite
import os.path
from filegenerator import files_in_folder_byext

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
    # Open the database and get the table name if none has been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if blobtable == "": blobtable = input("Insert table name:")
    
    my_connector = sqlite.connect(sql_filename)
    my_cursor    = my_connector.cursor()
    if not os.path.exists(sql_filename): print("File {0} does not exist.\n".format(sql_filename))
    
    else:
        # Build the instruction to be executed to create the table 
        instruction = """CREATE TABLE IF NOT EXISTS Blobtable(
        id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB, type TEXT, filename TEXT, searchterm TEXT);"""
        
        #Create the table
        my_cursor.execute(instruction)
        if printinstructions == True: print("Instruction executed:", instruction)
        
    # Commit the changes
    my_connector.commit()
    my_connector.close()
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
            instruction = """INSERT INTO {0} (data, type, filename) VALUES(?, ?, ?);""".format(blobtable)
            
            my_cursor.execute(instruction, (sqlite.Binary(ablob), ext, afile))
            if printinstructions == True: print("Instruction executed:", instruction)
    
    # Commit the changes
    my_connector.commit()
    my_connector.close()
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

    my_files = files_in_folder_byext (folder, extensions)
    
    for file in my_files:
        insert_blob(folder+file,
                    sql_filename,
                    blobtable,
                    printinstructions)
        
    
####################################################################################################

# def insert_searchterm