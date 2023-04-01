import openpyxl

# info to load workbook
directory_path = 'data/dodatkoweDane/xlms/' #remember to your path must end with /
file_name = 'dodatkowe próby do LUNG.xlsx'  #just file name with extension ex: data.xlsx

path = directory_path + file_name

# load workbook
workbook = openpyxl.load_workbook(path)

# get sheet names
sheet_names = workbook.sheetnames

# print sheet names
for sheet in sheet_names:
    print(sheet)
