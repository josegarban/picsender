import xlstocsv, xlsxtocsv

FILENAMES = ["test.xlsx", "test.xls"]

def test_getfirstrow(filenames):
    for filename in filenames:
        if filename.endswith(".xls"): xlstocsv.get_firstrow(filename)
        elif filename.endswith(".xlsx"): xlsxtocsv.get_firstrow(filename)
    
test_getfirstrow(FILENAMES)
 