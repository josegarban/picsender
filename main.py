import pprint
import credentials
import filegenerator, dbhandler
from dbchild import start_child, fill_child
from structures import listlist_to_dictdict
from userinput import choose_mode_populate, choose_mode_refine, input_filename
import xlstolist, xlsxtolist

####################################################################################################

def populate_db(mode = ""):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: call other functions to populate a database from a .xls or .xlsx file.
    Output: .sqlite database.
    """
    results = {}
    fieldvalues = []
    fieldnames = []
    
    if mode == "": mode = choose_mode_populate() # Usual state of affairs
        
    # Open the datasheet with the information and retrieve lists
    print("\nIn which workbook is the relevant table stored?")
    wb_filename     = input_filename()
    if wb_filename.endswith(".xlsx"):
        fieldnames  = xlsxtolist.get_firstrow (wb_filename)
        fieldvalues = xlsxtolist.get_otherrows(wb_filename)
    elif wb_filename.endswith(".xls"):
        fieldnames  = xlstolist.get_firstrow  (wb_filename)
        fieldvalues = xlstolist.get_otherrows (wb_filename)
    
    # Convert lists into a nested dictionary
    results = listlist_to_dictdict(fieldvalues, fieldnames)
    
    # Prepare the output file
    timestamp = filegenerator.generate_timestamp()

    if  mode["outputtype"][0] == "current.sqlite":
        filename = mode["outputtype"][1]
        results_mod = results
        dbhandler.update_dict_to_db(results_mod, filename, "Processed_infofile", "id", True)

    elif mode["outputtype"][0] == "fresh.sqlite":
        filename = mode["outputtype"][1] + "_" + timestamp + ".sqlite" 
        results_mod = results
        print("#"*100)
        pprint.pprint(results_mod)
        print("#"*100)
        dbhandler.create_table(results_mod, filename, "Processed_infofile", True)        
        dbhandler.add_dbrows(results_mod, filename, "Processed_infofile", "id", True)

    return results

####################################################################################################

def process_db(mode = ""):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: call other functions to populate a database from a .xls or .xlsx file.
    Output: refined .sqlite database.
    """
    if mode == "": mode = choose_mode_refine() # Usual state of affairs
    
    listcolumn_name        = mode["listcolumn_name"]
    additionalcolumn_names = mode["additionalcolumn_names"]
    separator              = mode["separator"]
    pythonic               = mode["pythonic"]
    sql_filename           = mode["sql_filename"]
    sql_table              = mode["sql_parenttable"]
    dbkey_column           = mode["parentdbkey_column"]
    sql_childtable         = mode["sql_childtable"]
    childfk_name           = mode["childfk_name"]
    printinstructions      = mode["printinstructions"]
    
    # Create the child table and generate a report
    start_child(sql_filename,
                  sql_table,
                  sql_childtable)
    
    fill_child (listcolumn_name,
                additionalcolumn_names,
                separator,
                pythonic,
                sql_filename,
                sql_table,
                dbkey_column,
                sql_childtable,
                childfk_name,
                printinstructions)
    
    
    
    return None


if __name__ == '__main__': process_db()