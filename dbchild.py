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
    instruction = """CREATE TABLE IF NOT EXISTS {0} {1}""".format(sql_childtable, fieldnames)
    
    # Create the table
    my_cursor.execute(instruction)
    if printinstructions == True: print("Instruction executed:", instruction)

    return None

####################################################################################################

def start_child(sql_filename, sql_parenttable, sql_childtable):
    """
    Inputs: filename, parent and child tables.
    Objective: create a child table with a foreign key from a parent table.
    Output: none besides those created by the called functions (logs).
    """
    print("\nA child table will be created in a .sqlite database with a foreign key from a parent table")
    if sql_filename    == "": sql_filename    = input("Insert file name:")
    if sql_parenttable == "": sql_parenttable = input("Insert parent table name:")
    if sql_childtable  == "": sql_childtable  = input("Insert child table name:")

    input_dict = dbhandler.get_alldbrows(sql_filename,
                               sql_parenttable,
                               "id",
                               True)
    
    parent_columns = dbhandler.get_alldbcolumns(sql_filename,
                               sql_parenttable,
                               "id",
                               True)
    
    relation_tuplist = get_relations(parent_columns)

    create_childtable(input_dict,
                      relation_tuplist,
                      sql_filename,
                      sql_parenttable,
                      sql_childtable,
                      True)
            
    return None
    
####################################################################################################
# ROW OPERATIONS
####################################################################################################

def parse_childvalues(listcolumn_name,
                      parent_dict,
                      separator = " ",
                      pythonic = False,
                      printinstructions = True):
    """
    Input: a column name containing string representations of lists,
            dictionary representing parent dictionary,
            whether the string representation is pythonic or not,
            separator in non-pythonic string representations
            printing instructions for some intermediate steps.
    Objective: take values from a table to create a secondary table
    Output: list of dictionaries 
    """
    output_dict = parent_dict
    
    # If parent_dict is a nested dictionary
    if type(output_dict[list(output_dict.keys())[0]]) is dict:
        for outer_key in output_dict:
            for inner_key in output_dict[outer_key]:
                if inner_key == listcolumn_name:
                    # Replace non-pythonic strings representing lists with lists
                    if pythonic == False:
                        input_string = output_dict[outer_key][inner_key]                        
                        output_dict[outer_key][inner_key] = structures.strspaces_to_simplelist(input_string,
                                                                                               separator)
                    else: pass
    else:
        for outer_key in output_dict:
            if outer_key == listcolumn_name:
                # Replace non-pythonic strings representing lists with lists
                if pythonic == False:
                    input_string = output_dict[outer_key]
                    output_dict[outer_key][inner_key] = structures.strspaces_to_simplelist(input_string,
                                                                                           separator)
                else: pass
    
    if printinstructions == True:
        print("\nDictionary where string representations of lists were turned into lists:")
        print(output_dict)
        
    return output_dict

####################################################################################################

def fill_child(listcolumn_name,
               additionalcolumn_names = "",
               separator = " ",
               pythonic = False,
               sql_filename = "",
               sql_table = "",
               dbkey_column = "id",
               sql_childtable = "",
               childfk_name = "parentid",
               printinstructions = True):
    """
    Inputs: a column name containing string representations of lists,
            additional column_names to be copied,
            whether the string representation is pythonic or not,
            filename,
            parent table that will be opened,
            id column name in parent table,
            child table that will be opened,
            id column name in child table,
            name of foreign key in child referencing the parent table,
            printinstructions will let some intermediate stepts to be reported on-screen
    Objective: get some values in a child table.
    Outputs: nested dictionary of the form { id value: {"column name": column value}...}.
    """
    output_string = ""
    
    # Get all values in parent table, ideally only some columns should be retrieved
    parent_dict = dbhandler.get_alldbrows(sql_filename,
                                          sql_table,
                                          dbkey_column,
                                          False)
    
    # Get the column names to be copied: if none are selected, all columns will be copied
    if additionalcolumn_names == "":
        additionalcolumn_names = dbhandler.get_alldbcolumns(sql_filename,
                                                            sql_table,
                                                            dbkey_column,
                                                            False)

    # Get the values to be copied in the new table
    child_dict = parse_childvalues(listcolumn_name,
                                   parent_dict,
                                   separator,
                                   pythonic,
                                   printinstructions)
    
    expanded_child_dict = structures.expand_dict(child_dict,
                                                 listcolumn_name,
                                                 childfk_name)

    # Open the database and get the table name if none has been set
    my_connector  = dbhandler.create_connector(sql_filename)
    my_cursor     = my_connector.cursor()
    if sql_childtable  == "": sql_table = input("Insert child table name to which values will be copied:")
    
    # Build the instruction to be executed to create the table
    fields_list    = dbhandler.dictfieldnames_to_tup(expanded_child_dict)
    fieldnames_str = dbhandler.dictfieldnames_to_string(expanded_child_dict)
    questionmarks  = "(" + (("?, ")*len(fields_list))[:-2] + ")"
    instruction    = """INSERT OR IGNORE INTO {0} {1} VALUES {2}""".format(
        sql_childtable, fieldnames_str, questionmarks)                 

    # Get the values in the instruction
    for outer_key in expanded_child_dict:    
        values     = [outer_key] # This is the id
        for value in expanded_child_dict[outer_key].values():
            values.append(value)
        
    # Execute the instruction
        row_string = "Instruction executed: {0} in table {1} in {2}.\nValues: {3}\n".format(
            instruction, sql_childtable, sql_filename, tuple(values))
        if printinstructions == True: print(row_string)
        my_cursor.execute(instruction, tuple(values))
        output_string = output_string + row_string
        
    # Commit and report the changes
    my_connector.commit()
    my_connector.close()
    
    # Generate report
    output_filename = sql_filename + "_history.txt"
    filegenerator.string_to_txt(output_filename, output_string)
    
    return output_string


    