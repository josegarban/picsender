from xlrd import open_workbook

def get_firstrow (filename, input_sheetname = ""):
    """
    Inputs: filename and optional input sheet name. If left blank, the first row will be read.
    Objective: get values in the first row, presumably column names.
    Output: list.
    """


    wb = open_workbook(filename, on_demand = True)
    sheetnames = wb.sheet_names()

    if input_sheetname == "":
        # Just get the first sheet
        ws = wb.sheet_by_name(sheetnames[0])
        fieldnames = ws.row_values(0)
        wb.unload_sheet(sheetnames[0])    
        print("Fieldnames found in sheet {0} in file {1}: ".format(sheetnames[0], filename), fieldnames)

    elif input_sheetname != "":
        if input_sheetname in sheetnames:
            ws = wb.sheet_by_name(input_sheetname)
            fieldnames = ws.row_values(1)
            wb.unload_sheet(input_sheetname)
            print("Fieldnames found in sheet {0} in file {1}: ".format(input_sheetname, filename), fieldnames)
        else:
            print("Sheet {0} not found in {1}.".format(input_sheetname, filename))

    return fieldnames