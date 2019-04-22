import pprint
import credentials
import blobmgr, filegenerator, dbhandler
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
        pprint.pprint(results)
        dbhandler.update_dict_to_db(results, filename, "rawdata", "id", True)

    elif mode["outputtype"][0] == "fresh.sqlite":
        filename = mode["outputtype"][1] + ".sqlite" 
        pprint.pprint(results)
        dbhandler.create_table(results, filename, "rawdata", True)        
        dbhandler.add_dbrows(results, filename, "rawdata", "id", True)

    return results

####################################################################################################

def process_db(mode = ""):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: call other functions to populate a database from a .xls or .xlsx file.
    Output: refined .sqlite database.
    """
    if mode == "": mode = choose_mode_refine() # Usual state of affairs
    
    relations = (mode["parentdbkey_column"],
                 mode["sql_parenttable"],
                 mode["sql_parenttable"] + mode["parentdbkey_column"])
    
    # Create the child table and generate a report
    start_child(mode["sql_filename"],
                mode["sql_parenttable"],
                mode["sql_childtable"],
                relations)
    
    fill_child (mode["listcolumn_name"],
                mode["additionalcolumn_names"],
                mode["separator"],
                mode["pythonic"],
                mode["sql_filename"],
                mode["sql_parenttable"],
                mode["parentdbkey_column"],
                mode["sql_childtable"],
                mode["childfk_name"],
                mode["printinstructions"])

    # Create the blobtable
    blobmgr.add_blobtable(mode["sql_filename"],
                          "blobtable",
                          mode["printinstructions"])
    blobmgr.insert_blobs("",
                         mode["blobfolder"],
                         mode["sql_filename"],
                         "blobtable",
                         mode["printinstructions"])
    blobmgr.insert_searchterm(mode["searchdirection"],
                              mode["searchchars"],
                              mode["sql_filename"],
                              "blobtable",
                              "id",
                              mode["printinstructions"])

    return None


if __name__ == '__main__':
    populate_db()
    process_db()
    
