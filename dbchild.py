"""
Sqlite functions to create a child table to a parent table in the database
"""

import dbhandler
import structures

####################################################################################################
# INSTRUCTION CREATION 
####################################################################################################

def get_relations(field_list, table_names = ""):
    """
    Input: field list in the dictionary from where the relations will be used
            table_names (optional): list of tables in a sql database.
    Objective: define a foreign key.
    Output: list with a tuple of the form (fieldname, referencetable_name, fieldname_in_referencetable) 
            to be used in statements such as:
            "id integer NOT NULL,
                FOREIGN KEY (id) REFERENCES parent_table(id)".
    """
    templist = ["", "", ""]

    if table_names != "": print("\nThe following tables exist in the database", table_names)
    print("\nOne of the tables in the database will be linked to a child table to be created.")
    print("Which of the following fields in the parent table will exist in both tables?")
    print(field_list, "\n")
    templist[0] = input("Type the field here: ")
    print("What is the parent table to the child table that will be created?")
    templist[1] = input("Type the name here: ")
    print("What is this field called in the parent table? Leave it blank if it is called the same in both: ")
    templist[2] = input("Type the name here: ")
    
    return tuple(templist)
    
####################################################################################################

def tuplists_merge(tuplist1, tuplist2="", mergeby1 = 0, mergeby2 = 0):
    """
    Input: field list containing tuples
            the user will be prompted for a secondary list containing tuples
            to be merged with the first if it is not provided,
            mergeby is the index in the primary_tuplist by which both tuple lists will be merged.
    Objective: add values to the tuples of a list containing tuples provided that the tuples in both lists
            share a variable
    Output: field list containing tuples adding other characteristics or keywords from relations_list
    """
    output_tuplist = []
    if tuplist2 == "" : tuplist2 = get_relations(tuplist1)
    
    for tuplist1_tup in tuplist1:
        # Each tuple in the primary list is converted into a temporary list to which characterstics
        # in the tuples coming from the secondary list will be added.
        templist = [x for x in tuplist1_tup] 
        for tuplist2_tup in tuplist2:
            if tuplist1_tup[mergeby1] == tuplist2_tup[mergeby2]:
                for characteristic in tuplist2_tup:
                    templist.append(characteristic)
        output_tuplist.append(tuple(templist))
    
    return output_tuplist

####################################################################################################

def child_dictfields_to_string(input_dict, relations_list):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dbhandler.dictfieldnames_to_tuplist(input_dict)
    # New function returning a tuple of len n   
    fieldsrelations_list = tuplists_merge(field_list, relations_list) 

    output_string = ""
    for field_tup in fieldsrelations_list:
        field_string = ""
        for value in field_tup:
            #improvement on .format method in dbhandler.dictfields_to_string
            field_string = field_string + str(value) + " "
        output_string = output_string + field_string + ", "
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space
    
    return output_string

####################################################################################################
# ADDING CHILD TABLES
####################################################################################################

def create_childtable(input_dict,
                      relation_tuplist,
                      sql_filename = "",
                      sql_table = "",
                      sql_childtable = "",
                      printinstructions = True):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: a table in a sql table will be created but not filled with data,
            based on the dictionary.
    Outputs: none.
    """

    # Open the database and get the table name if none has been set
    my_connector = dbhandler.create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert parent table name:")
    if sql_childtable == "": sql_childtable = input("Insert child table name:")

    # Build the instruction to be executed to create the table 
    fieldnames = child_dictfields_to_string(input_dict, relation_tuplist)
    print("Fieldnames,", fieldnames)
    instruction = """CREATE TABLE IF NOT EXISTS {0} {1}""".format(sql_childtable, fieldnames)
    
    # Create the table
    my_cursor.execute(instruction)
    if printinstructions == True: print("Instruction executed:", instruction)

    return None
    