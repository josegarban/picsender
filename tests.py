import main
import dbchild, dbhandler
import xlstolist, xlsxtolist
from pprint import pprint

FILENAMES = ["test.xlsx", "test.xls"]

####################################################################################################
######################################## TEST LOADING DATA ######################################### 
####################################################################################################

def test_get_firstrow(filenames, input_sheetname = ""):
    print("Testing getting the first row in the test files with a sheet name.")
    for filename in filenames:
        if filename.endswith(".xls"): xlstolist.get_firstrow(filename, input_sheetname)
        elif filename.endswith(".xlsx"): xlsxtolist.get_firstrow(filename, input_sheetname)
    print("")

    print("Testing getting the first row in the test files, first sheet.")
    for filename in filenames:
        if filename.endswith(".xls"): xlstolist.get_firstrow(filename, "")
        elif filename.endswith(".xlsx"): xlsxtolist.get_firstrow(filename, "")
    print("")


def test_get_otherrows(filenames, input_sheetname = ""):
    print("Testing getting the remaining rows in the test files with a sheet name.")
    for filename in filenames:
        if filename.endswith(".xls"):
            print("\nFiletype: .xls:")
            test = xlstolist.get_otherrows(filename, input_sheetname)
            pprint(test)
        elif filename.endswith(".xlsx"):
            print("\nFiletype: .xlsx:")
            test = xlsxtolist.get_otherrows(filename, input_sheetname)
            pprint(test)
    print("")
    print("Testing getting the remaining rows in the test files, first sheet.")
    for filename in filenames:
        if filename.endswith(".xls"):
            print("\nFiletype: .xls:")
            test = xlstolist.get_otherrows(filename, "")
            pprint(test)
        elif filename.endswith(".xlsx"):
            print("\nFiletype: .xlsx:")
            test = xlsxtolist.get_otherrows(filename, "")
            pprint(test)
    print("")

#test_get_firstrow(FILENAMES, input_sheetname = "Feuille1")
#test_get_otherrows(FILENAMES, input_sheetname = "Feuille1") 
 
#main.populate_db()

####################################################################################################
################################### TEST CHILDREN CREATION ######################################### 
####################################################################################################

def test_dbchild(sql_filename, sql_parenttable, sql_childtable):
    
    input_dict = dbhandler.get_alldbrows(sql_filename,
                               sql_parenttable,
                               "id",
                               True)
    
    parent_columns = [x[0] for x in dbhandler.dictfieldnames_to_tuplist(input_dict)]
    print("Columns", parent_columns)
    
    parent_keys = dbhandler.get_alldbkeys(sql_filename,
                              sql_parenttable,
                              "id",
                              True)
    
    relation_tuplist = dbchild.get_relations(parent_columns)
    
    dbchild.create_childtable(input_dict,
                              relation_tuplist,
                              sql_filename,
                              sql_parenttable,
                              sql_childtable,
                              True)
            
    return None

####################################################################################################

FILENAME = "output.sqlite"
PARENTTABLE = "Processed_infofile"
CHILDTABLE = "Child"

test_dbchild(FILENAME, PARENTTABLE, CHILDTABLE)