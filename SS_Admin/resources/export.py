import xlsxwriter

from . import var_const as vc

excel_doc = None

def export_to_excel():
    global excel_doc
    excel_doc = xlsxwriter.Workbook(f"{vc.active_year}_{vc.active_camp}-report.xlsx")
    
    __export_campers()
    __export_staff()
    __export_bank()
    __export_history()
    
    excel_doc.close()
    pass

def __export_campers():
    global excel_doc
    camper_sheet = excel_doc.add_worksheet("Camper Accounts")
    
    
    pass

def __export_staff():
    global excel_doc
    staff_sheet = excel_doc.add_worksheet("Staff Accounts")
    pass

def __export_bank():
    global excel_doc
    bank_sheet = excel_doc.add_worksheet("Bank Data")
    pass

def __export_history():
    global excel_doc
    history_sheet = excel_doc.add_worksheet("Transaction History")
    pass