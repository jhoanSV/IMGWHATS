import openpyxl

def read_excel_file(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    data = []
    
    for row in sheet.iter_rows(values_only=True):
        name = row[0]
        number = row[1]
        data.append({'ferreteria': name, 'numero': number})
    
    return data

# Specify the path to your Excel file
excel_file_path = './Numero_mensaje_whatsapp.xlsx'

# Read the Excel file and get the data as a dictionary
excel_data = read_excel_file(excel_file_path)
print(excel_data)

