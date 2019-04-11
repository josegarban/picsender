from openpyxl import load_workbook, Workbook

def get_firstrow (filename, input_sheetname = ""):
    """
    Inputs: filename and optional input sheet name. If left blank, the first row will be read.
    Objective: get values in the first row, presumably column names.
    Output: list.
    """

    wb = load_workbook(filename)
    sheetnames = wb.sheetnames

    if input_sheetname == "":
        # Just get the first sheet
        ws = wb[sheetnames[0]]
        fieldnames = []
        for row in ws.iter_rows(min_row=0, max_row=1, values_only=True):
            for cell in row:
                fieldnames.append(cell)
        
        print("Fieldnames found in sheet {0} in file {1}: ".format(sheetnames[0], filename), fieldnames)

    elif input_sheetname != "":
        if input_sheetname in sheetnames:
            ws = wb[sheetnames[input_sheetname]]
            fieldnames = ws['A']
            
            print("Fieldnames found in sheet {0} in file {1}: ".format(input_sheetname, filename), fieldnames)
        else:
            print("Sheet {0} not found in {1}.".format(input_sheetname, filename))

    return fieldnames