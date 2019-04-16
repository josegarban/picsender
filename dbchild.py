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
    templist[1] = ", FOREIGN KEY (" + templist[1] + ")"
    print("What is this field called in the parent table? Leave it blank if it is called the same in both: ")
    templist[2] = input("Type the name here: ")
    templist[2] = "REFERENCES (" + templist[2] + ")"
    print("")
    
    return tuple(templist)
    
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
    print("")
    
    desc = "INTEGER NOT NULL, FOREIGN KEY ({0}) REFERENCES {1}({2})".format(templist[0],
                                                                          templist[1],
                                                                          templist[2])

    return [(templist[0], desc)]

####################################################################################################

def tuplists_merge(tuplist1, tuplist2="", mergeby1 = 0, mergeby2 = 0,
                    printinstructions = True):
    """
    Input: field list containing tuples
            the user will be prompted for a secondary list containing tuples
            to be merged with the first if it is not provided,
            mergeby is the index in the primary_tuplist by which both tuple lists will be merged,
            printinstructions will let some intermediate stepts to be reported on-screen.
    Objective: add values to the tuples of a list containing tuples provided that the tuples in both lists
            share a variable
    Output: field list containing tuples adding other characteristics or keywords from relations_list
    """
    output_tuplist = []
    if tuplist2 == "" : tuplist2 = get_relations(tuplist1)
    
    for tuplist1_tup in tuplist1:
        """
        Each tuple in the primary list is converted into a temporary list to which characterstics
        In the tuples coming from the secondary list will be added.
        """
        templist = [x for x in tuplist1_tup] # Components kept as lists so that they can be modified
        
        if templist[mergeby1] == tuplist2[mergeby2]:
            for characteristic in tuplist2[:mergeby2-1]:
                templist.append(characteristic)
            for characteristic in tuplist2[mergeby2+1:]:
                templist.append(characteristic)
        output_tuplist.append(templist) 
    
    for tuplist2_tup in tuplist2:
        if list(tuplist2_tup) not in output_tuplist:
            output_tuplist.append(tuplist2_tup)
    
    for templist in output_tuplist:
        templist = tuple(templist) # Components converted to tuples again

    if printinstructions == True:
        print("List 1 to be merged:", tuplist1)
        print("List 2 to be merged:", tuplist2)
        print("Merged by indices:", mergeby1, "in list 1 and", mergeby2, "in list 2.")
        print("Result:", output_tuplist)
        print("\n")

    return output_tuplist

####################################################################################################

def child_dictfields_to_string(input_dict,
                               relations_list,
                               printinstructions = True): ###Change this function
    """
    Inputs: dictionary with the parent table.
            list with the parameters in the child table,
            printinstructions will let some intermediate stepts to be reported on-screen.
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
    
    if printinstructions == True:
        print("Converting the following dictionary to string:", input_dict)
        print("Merging the following list with the dictionary:", relations_list)
        print("Output:", output_string)
        print("\n")
    
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
            The table won't be created if it already exists
            printinstructions will let some intermediate stepts to be reported on-screen.
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
    if printinstructions == True: print("Instruction executed:", instruction)
    my_cursor.execute(instruction)
    if printinstructions == True: print("Instruction executed:", instruction)

    return None
    