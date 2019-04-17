import sqlite3 as sqlite

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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file BLOB,
        type TEXT,
        filename TEXT,
        searchterm TEXT);"""
        
        #Create the table
        my_cursor.execute(instruction)
        if printinstructions == True: print("Instruction executed:", instruction)
    return None

