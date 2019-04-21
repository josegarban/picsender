"""
Sqlite functions
"""

import sqlite3
import userinput
import pprint
import structures
import filegenerator

####################################################################################################
# INSTRUCTION CREATION 
####################################################################################################

def dictfieldnames_to_tuplist(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: list containing tuples of the form (fieldname, fieldtype)
    """
    output_list = []
    
    # Check if the primary key is an integer or a string
    primarykey_istext = True
    for outer_key in input_dict.keys():
        try:
            if type(outer_key) is int: primarykey_istext = False
        except:
            primarykey_istext = True
            continue # At the first sight of a non-integer key, the loop will end
    
    if   primarykey_istext: output_list.append(("id", "VARCHAR(32) PRIMARY KEY"))
    else                  : output_list.append(("id", "INTEGER PRIMARY KEY"))
    
    # Search all inner dictionaries in a dictionary
    for outer_key in input_dict:  # It should not matter if the dictionary contains dictionaries or a list            
        for inner_key in input_dict[outer_key]:
            fieldname = str(inner_key)
        
            if   type(input_dict[outer_key][inner_key]) is int  : fieldtype = "INTEGER"
            elif type(input_dict[outer_key][inner_key]) is str  : fieldtype = "TEXT"
            elif type(input_dict[outer_key][inner_key]) is bool : fieldtype = "BINARY"
            elif type(input_dict[outer_key][inner_key]) is float: fieldtype = "REAL"
            # No plans to fully use RMDB at the moment, other data types will be converted to text
            elif type(input_dict[outer_key][inner_key]) is list : fieldtype = "TEXT"
            elif type(input_dict[outer_key][inner_key]) is tuple: fieldtype = "TEXT"
            elif type(input_dict[outer_key][inner_key]) is dict : fieldtype = "TEXT"
            else : fieldtype = "TEXT"
        
            if   (fieldname, fieldtype) not in output_list : output_list.append((fieldname, fieldtype))
    
    return output_list

####################################################################################################

def dictfieldnames_to_tup(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: tuple containing fieldnames only
    """
    fieldfullinfo = dictfieldnames_to_tuplist(input_dict)
    fieldnames = [x[0] for x in fieldfullinfo]
    
    return tuple(fieldnames)

####################################################################################################

def dictfields_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)
    
    output_string = ""
    for field_tup in field_list:
        field_string = "{0} {1}, ".format(field_tup[0], field_tup[1])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space
    
    return output_string

####################################################################################################

def dictfieldnames_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets field names in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)
    
    output_string = ""
    for field_tup in field_list:
        field_string = "{0}, ".format(field_tup[0])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space
    
    return output_string

####################################################################################################
# SQL MANIPULATION 
####################################################################################################

def create_connector(sql_filename = ""):
    """
    Inputs: filename or path.
    Objective: open the sqlite database.
    Outputs: connector.
    """

    # Get the filename if none has been set
    if sql_filename == "": sql_filename = userinput.input_filename()    

    # Open the Sqlite database we're going to use (my_cursor)
    my_connector = sqlite3.connect(sql_filename)

    return my_connector

####################################################################################################
# ADDING TABLES
####################################################################################################

def create_table(input_dict, sql_filename = "", sql_table = "", printinstructions = True):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: a table in a sql table will be created but not filled with data,
            based on the dictionary.
    Outputs: none.
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to create the table 
    fieldnames = dictfields_to_string(input_dict)
    instruction = """CREATE TABLE IF NOT EXISTS {0} {1}""".format(sql_table, fieldnames)
    
    # Create the table
    my_cursor.execute(instruction)
    if printinstructions == True: print("Instruction executed:", instruction)

    return None
    
####################################################################################################
# FUNCTIONS TO COMPARE DATA IN A DICTIONARY AND DATA IN A TABLE DATABASE
####################################################################################################

def get_alldbcolumns(sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get all column names in a database table.
    Outputs: list with column names in the database table.
    """
    
    input_dict = get_alldbrows(sql_filename,
                               sql_table,
                               dbkey_column,
                               printinstructions)
    output_list = [x[0] for x in dictfieldnames_to_tuplist(input_dict)]
    
    if printinstructions == True: print("Columns in table '{0}' in file '{1}': {2}".format(sql_table,
                                                                                           sql_filename,
                                                                                           output_list))
    
    return output_list

####################################################################################################

def get_alldbkeys(sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get all keys in a database table.
    Outputs: list with keys in the database table.
    """

    # Open the database and get the table name if none has been set
    my_connector  = create_connector(sql_filename)
    my_cursor     = my_connector.cursor()
    if sql_table  == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction   = """SELECT {0} FROM {1}""".format(dbkey_column, sql_table)                 

    # Execute the instruction to get a tuple for each table row
    my_cursor.execute(instruction)
    dbvalues_tups = my_cursor.fetchall()
    
    # Create and report the output
    output_list   = [x[0] for x in dbvalues_tups]
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} keys found in database: \n{3}\n".format(
            instruction, sql_filename, len(output_list), output_list))    

    return output_list

####################################################################################################

def get_alldbrows(sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get all values in a database table.
    Outputs: nested dictionary of the form { id value: {"column name": column value}...}.
    """
    # Open the database and get the table name if none has been set
    my_connector  = create_connector(sql_filename)
    my_cursor     = my_connector.cursor()
    if sql_table  == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to get the keys in the database
    instruction   = """SELECT * FROM {0}""".format(sql_table)                 

    # Execute the instruction
    dbvalues_tups = [x for x in my_cursor.execute(instruction)]

    #Find the index of the key (probably "id") in the database table
    db_colnames   = [x[0] for x in my_cursor.description]
    keycol_index  = db_colnames.index(dbkey_column)
    
    # Convert the tuples from the database into a dictionary of the form {"id" {"values": values}}
    output_dict = {}
    for tup in dbvalues_tups:
        output_dict[tup[keycol_index]] = {}
        for col in db_colnames:
            if col != dbkey_column: # key column (probably "id") is outside the inner dictionary
                output_dict[tup[keycol_index]][col] = tup[db_colnames.index(col)]
    
    # Report the output
    if printinstructions == True:
        print("Instruction executed: {0} in {1}.\n{2} rows found in database: \n{3}\n".format(
            instruction, sql_filename, len(output_dict), output_dict))    
    
    return output_dict
    
####################################################################################################

def compare_keysonly(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
    Outputs: tuple of the form (are values the same?, which values are different).
    """

    # Get the keys in the dictionary and in the database table
    dictvalues_list = structures.getdictkeys(input_dict)        
    dbvalues_list = get_alldbkeys(sql_filename, sql_table, dbkey_column, printinstructions)

    # Get what is in one list but not in the other
    actual_comparison = structures.compare_twolists(dictvalues_list, dbvalues_list, "dictionary", "database", printinstructions)
    
    return actual_comparison

####################################################################################################

def compare_keysfull(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
            However, different values besides "id" are not compared.
    Outputs: tup of the form (are values the same?, which values are different).
    """

    # Convert the table into a dictionary to compare with input_dict
    db_dict = get_alldbrows(sql_filename, sql_table, dbkey_column, printinstructions)

    # Describe the dictionary
    structures.print_dictdescription(input_dict, "database dictionary", printinstructions)    

    # Compare the dictionaries
    actual_comparison = structures.compare_twodictkeys(input_dict,
                                                       db_dict,
                                                       "input dictionary",
                                                       "database dictionary")
    
    return actual_comparison

####################################################################################################

def compare_rowsfull(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare full rows in the dictionary against values in the table.
            Values other than "id" are compared.
    Output: tuple of the form  (rows in dictionary not in database,
                                rows in database not in dictionary,
                                rows in both which are different).
    """

    # Convert the table into a dictionary to compare with input_dict
    db_dict = get_alldbrows(sql_filename, sql_table, dbkey_column, printinstructions)

    # Describe the dictionary
    structures.print_dictdescription(input_dict, "input dictionary", printinstructions)    

    # Compare the dictionaries
    actual_comparison = structures.compare_twodictsfull(input_dict,
                                                       db_dict,
                                                       "input dictionary",
                                                       "database dictionary")
    
    return actual_comparison

####################################################################################################
# ROW OPERATIONS
####################################################################################################

def add_dbrows(input_dict,
               sql_filename = "",
               sql_table = "",
               dbkey_column = "id",
               printinstructions = True):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
    Objective: a table in a sql table will be filled with data,
                or edited if existing, from a dictionary.
    Outputs: string reporting changes.
    """
    output_string = ""
    
    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to create the table
    fields_list    = dictfieldnames_to_tup(input_dict)
    fieldnames_str = dictfieldnames_to_string(input_dict)
    questionmarks  = "(" + (("?, ")*len(fields_list))[:-2] + ")"
    instruction    = """INSERT OR IGNORE INTO {0} {1} VALUES {2}""".format(
        sql_table, fieldnames_str, questionmarks)                 

    # Get the values in the instruction
    for outer_key in input_dict:    
        values     = [outer_key] # This is the id
        for value in input_dict[outer_key].values():
            values.append(value)
        
    # Execute the instruction
        row_string = "Instruction executed: {0} in table {1} in {2}.\nValues: {3}\n".format(
            instruction, sql_table, sql_filename, tuple(values))
        if printinstructions == True: print(row_string)
        my_cursor.execute(instruction, tuple(values))
        output_string = output_string + row_string
        
    # Commit and report the changes
    my_connector.commit()
    my_connector.close()
    
    return output_string

####################################################################################################

def remove_dbrows(input_dict,
                  sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: list of ids to find the rows that will be removed,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
    Outputs: string reporting changes.
    """
    
    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # Build the instruction to be executed to remove rows 
    instruction = """DELETE FROM {0} WHERE {1} = ?""".format(sql_table, dbkey_column)
    
    # Get the rows that will be removed
    values = tuple([x for x in input_dict.keys()])
    
    # Execute the instruction
    my_cursor.execute(instruction, values)
    if len(input_dict) == 0:
        output_string = "No rows removed in {0}".format(sql_filename)
    else:
        output_string = "Instruction executed: {0} in table {1} in {2}.\nValues: {3}\n".format(
            instruction, sql_table, sql_filename, input_dict)    

    # Commit and report the changes
    my_connector.commit()
    my_connector.close()
    if printinstructions == True: print(output_string)
    
    return output_string

####################################################################################################

def update_dbrows(input_dict,
                  sql_filename = "",
                  sql_table = "",
                  dbkey_column = "id",
                  printinstructions = True):
    """
    Inputs: list of ids to find the rows that will be updated,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
    Outputs: string reporting changes.
    """
    output_string = ""
    
    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    #Find the index of the key (probably "id") in the database table
    instruction   = """SELECT * FROM {0}""".format(sql_table)
    my_cursor.execute(instruction)
    db_colnames   = [x[0] for x in my_cursor.description]
    keycol_index  = db_colnames.index(dbkey_column)
    
    # This should look like: "Field 1 = ?, ... Field n = ?" excluding the field with the key
    setfields = "".join(x + " = ?, "  for x in db_colnames if db_colnames.index(x) != keycol_index)[:-2]

    # Build the instruction to be executed to remove rows 
    instruction = """UPDATE {0} SET {1} WHERE {2} = ?""".format(sql_table, setfields, dbkey_column)
    print(input_dict) 

    # Get the values in the instruction
    values = []
    for outer_key in input_dict:    
        values = list(input_dict[outer_key][0].values()) # index 0 because index 1 = old values
        values.append(outer_key) # id goes at the end because it goes after "WHERE"

    # Execute the instruction
        my_cursor.execute(instruction, tuple(values))
        row_string = "Instruction executed: {0} in table {1} in {2}.\nValues: {3}\n".format(
            instruction, sql_table, sql_filename, tuple(values))
        output_string = output_string + row_string

    # Commit and report the changes
    my_connector.commit()
    my_connector.close()
    if printinstructions == True: print(output_string)
    
    return output_string

####################################################################################################
# DATABASE UPDATES
####################################################################################################

def update_dict_to_db(input_dict,
                     sql_filename = "",
                     sql_table = "",
                     dbkey_column = "id",
                     printinstructions = True):
    """
    Inputs: dictionary that will be compared with the database,
            filename,
            table that will be opened,
            column in the database table is assumed to be called "id", (can be changed)
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: compare keys in the dictionary against values in the table.
    Outputs: change report exported to a txt file.
    """
    
    # Get the file and table name if none have been set
    if sql_filename == "": sql_filename = input("Insert file name:")
    if sql_table    == "": sql_table = input("Insert table name:")
    
    # Get the differences
    discrepancies = compare_rowsfull(input_dict,
                                     sql_filename,
                                     sql_table,
                                     dbkey_column,
                                     printinstructions)

    # Rows in input_dict but not in database: discrepancies[0], these will be added
    if printinstructions == True: print("Adding rows...")
    string1 = add_dbrows(discrepancies[0],
                         sql_filename,
                         sql_table,
                         dbkey_column,
                         printinstructions)
    
    # Rows in database but not in input_dict: discrepancies[1], these will be deleted
    if printinstructions == True: print("Removing rows...")
    string2 = remove_dbrows(discrepancies[1],
                            sql_filename,
                            sql_table,
                            dbkey_column,
                            printinstructions)
    
    # Rows in both with different values    : discrepancies[2][0], these will be updated
    if printinstructions == True: print("Updating rows...")
    string3 = update_dbrows(discrepancies[2],
                            sql_filename,
                            sql_table,
                            dbkey_column,
                            printinstructions)
    
    # Generate report
    output_string = filegenerator.generate_timestamp() + "\n"*2 + string1 + string2 + string3
    output_filename = sql_filename + "_history.txt"
    filegenerator.string_to_txt(output_filename, output_string)
    
    return None
