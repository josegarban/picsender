import main
import dbchild, dbhandler, structures
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

FILENAME = "output.sqlite"
PARENTTABLE = "Processed_infofile"
CHILDTABLE = "Child"
CHILDCOLUMN = ("Fotos")

#dbchild.startchild(FILENAME, PARENTTABLE, CHILDTABLE)
dbchild.fill_child(CHILDCOLUMN,
                   "",
                   " ",
                   False,
                   FILENAME,
                   PARENTTABLE,
                   "id",
                   CHILDTABLE,
                   "parentid",
                   True)

####################################################################################################

MYLIST = [0, 10, 20, 30, 40]
MYCHOICE1 = [10, 30]
MYCHOICE2 = [1, 3]
MYCHOICE3 = ["a", "b"]

def test_structures_sieves(input_list, input_choice1, input_choice2):
    print("Testing removing members from a list with a predetermined choice...")
    structures.keep_members_inlist(input_list, input_choice1)
    print("")
    print("Testing removing members from a list with an inconsistent predetermined choice...")
    structures.keep_members_inlist(input_list, input_choice2)
    print("")
    print("Testing removing members from a list with a user-defined choice...")
    structures.keep_members_inlist(input_list, "")
        
#test_structures_sieves(MYLIST, MYCHOICE1, MYCHOICE2)