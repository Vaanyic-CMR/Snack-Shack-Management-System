from tkinter import messagebox
import xlsxwriter

from .models import (
    camper as camper_model,
    staff as staff_model,
    bank as bank_model,
    history as history_model
)

from . import var_const as vc

excel_doc = None
bold = None
money = None

head_row = None
head_money = None
error_format = None
warning_format = None

align_left = None

def eow_check():
    if vc.active_camp not in [ "trekker", "pathfinder", "journey", "trail blazer", "navigator" ]:
        raise Exception("Invalid camp selected")
    
    campers = camper_model.Camper.get_all_by_camp(vc.active_camp)
    
    bad_accounts = list()
    for idx, camper in enumerate(campers):
        if camper.eow_remainder == "donate":
            campers[idx].total_donated += camper.curr_bal
            campers[idx].curr_bal = 0
            camper_model.Camper.update(campers[idx].to_dict())
        elif camper.eow_remainder != "donate" and camper.curr_bal > 0:
            bad_accounts.append(camper)
    
    return bad_accounts

def export_to_excel():
    if vc.active_camp not in [ "trekker", "pathfinder", "journey", "trailblazer", "navigator" ]:
        messagebox.showerror("Value Error", "Invalid camp selected")
        raise Exception("Invalid camp selected")
    
    global excel_doc
    excel_doc = xlsxwriter.Workbook(f"databases/reports/{vc.active_year}_{vc.active_camp}-snack_shack_report.xlsx")
    
    # Cell Formating
    global bold, money, align_left, head_row, head_money, error_format, warning_format
    bold = excel_doc.add_format({'bold': True})
    
    money = excel_doc.add_format({'num_format': '[$$-409]#,##0.00'})
    money.set_align("left")
    
    align_left = excel_doc.add_format()
    align_left.set_align("left")
    head_row = excel_doc.add_format()
    head_row.set_bg_color("silver")
    head_row.set_align("left")
    head_money = excel_doc.add_format({'num_format': '[$$-409]#,##0.00'})
    head_money.set_bg_color("silver")
    head_money.set_align("left")
    
    warning_format = excel_doc.add_format()
    warning_format.set_bg_color("orange")
    error_format = excel_doc.add_format()
    error_format.set_bg_color("red")
    
    __export_campers()
    __export_staff()
    __export_bank()
    __export_history()
    
    excel_doc.close()
    messagebox.showinfo("Notice", "Export Successful")
    pass

def __export_campers():
    global excel_doc, bold, money, error_format, warning_format
    camper_sheet = excel_doc.add_worksheet("Camper Accounts")
    
    campers = camper_model.Camper.get_all_sort_camp_gender_name()
    
    # Adjust the column width.
    camper_sheet.set_column('B:B', 20)
    camper_sheet.set_column('E:G', 15)
    camper_sheet.set_column('I:I', 15)
    camper_sheet.set_column('J:J', 25)
    camper_sheet.set_column('K:L', 30)
    
    # Row Titles
    camper_sheet.write("A3", "ID", bold)
    camper_sheet.write("B3", "Name", bold)
    camper_sheet.write("C3", "Gender", bold)
    camper_sheet.write("D3", "Camp", bold)
    camper_sheet.write("E3", "Payment Method", bold)
    camper_sheet.write("F3", "Initial Balance", bold)
    camper_sheet.write("G3", "Current Balance", bold)
    camper_sheet.write("H3", "Spent", bold)
    camper_sheet.write("I3", "Total Donated", bold)
    camper_sheet.write("J3", "End of Week Return", bold)
    camper_sheet.write("K3", "Last Purchase", bold)
    camper_sheet.write("L3", "Parent EOW Remainder", bold)
    
    row = 4
    for camper in campers:
        camper_sheet.write(f"A{row}", camper.id, align_left)
        camper_sheet.write(f"B{row}", camper.name, align_left)
        camper_sheet.write(f"C{row}", camper.gender, align_left)
        camper_sheet.write(f"D{row}", camper.camp, align_left)
        camper_sheet.write(f"E{row}", camper.pay_method, align_left)
        camper_sheet.write(f"F{row}", camper.init_bal, align_left)
        camper_sheet.write(f"G{row}", camper.curr_bal, align_left)
        camper_sheet.write(f"H{row}", camper.curr_spent, align_left)
        camper_sheet.write(f"I{row}", camper.total_donated, align_left)
        camper_sheet.write(f"J{row}", camper.eow_return, align_left)
        camper_sheet.write(f"K{row}", camper.last_purchase, align_left)
        camper_sheet.write(f"L{row}", camper.eow_remainder, align_left)
        row += 1
    
    # Summing Data Functions
    camper_sheet.write("A2", "Account Sums", bold)
    camper_sheet.write("F2", f"=SUM(F4:F{row})", money)
    camper_sheet.write("G2", f"=SUM(G4:G{row})", money)
    camper_sheet.write("H2", f"=SUM(H4:H{row})", money)
    camper_sheet.write("I2", f"=SUM(I4:I{row})", money)
    camper_sheet.write("J2", f"=SUM(J4:J{row})", money)
    
    camper_sheet.conditional_format(
        'G2:G2',
        {
            'type': 'cell',
            'criteria': '>',
            'value': 0,
            'format': warning_format
        }
    )
    camper_sheet.conditional_format(
        f'G4:G{row}',
        {
            'type': 'cell',
            'criteria': '>',
            'value': 0,
            'format': error_format
        }
    )
    pass
def __export_staff():
    global excel_doc, bold, money, error_format, warning_format
    staff_sheet = excel_doc.add_worksheet("Staff Accounts")
    
    staffers = staff_model.Staff.get_all()
    
    # Adjust the column width.
    staff_sheet.set_column('B:D', 20)
    staff_sheet.set_column('E:E', 30)
    staff_sheet.set_column('F:G', 15)
    staff_sheet.set_column('I:I', 15)
    staff_sheet.set_column('J:J', 25)
    staff_sheet.set_column('K:L', 30)
    
    # Row Titles
    staff_sheet.write("A3", "ID", bold)
    staff_sheet.write("B3", "Name", bold)
    staff_sheet.write("C3", "Payment Method", bold)
    staff_sheet.write("D3", "# of Free Items", bold)
    staff_sheet.write("E3", "Last Free Item", bold)
    staff_sheet.write("F3", "Initial Balance", bold)
    staff_sheet.write("G3", "Current Balance", bold)
    staff_sheet.write("H3", "Spent", bold)
    staff_sheet.write("I3", "Total Donated", bold)
    staff_sheet.write("J3", "End of Season Return", bold)
    staff_sheet.write("K3", "Last Purchase", bold)
    
    row = 4
    for staff in staffers:
        staff_sheet.write(f"A{row}", staff.id, align_left)
        staff_sheet.write(f"B{row}", staff.name, align_left)
        staff_sheet.write(f"C{row}", staff.pay_method, align_left)
        staff_sheet.write(f"D{row}", staff.num_of_free_items, align_left)
        staff_sheet.write(f"E{row}", staff.last_free_item, align_left)
        staff_sheet.write(f"F{row}", staff.init_bal, align_left)
        staff_sheet.write(f"G{row}", staff.curr_bal, align_left)
        staff_sheet.write(f"H{row}", staff.curr_spent, align_left)
        staff_sheet.write(f"I{row}", staff.total_donated, align_left)
        staff_sheet.write(f"J{row}", staff.eos_return, align_left)
        staff_sheet.write(f"K{row}", staff.last_purchase, align_left)
        row += 1
    
    # Summing Data Functions
    staff_sheet.write("A2", "Account Sums", bold)
    staff_sheet.write("F2", f"=SUM(F4:F{row})", money)
    staff_sheet.write("G2", f"=SUM(G4:G{row})", money)
    staff_sheet.write("H2", f"=SUM(H4:H{row})", money)
    staff_sheet.write("I2", f"=SUM(I4:I{row})", money)
    staff_sheet.write("J2", f"=SUM(J4:J{row})", money)
    
    staff_sheet.conditional_format(
        'G2:G2',
        {
            'type': 'cell',
            'criteria': '>',
            'value': 0,
            'format': warning_format
        }
    )
    staff_sheet.conditional_format(
        f'G4:G{row}',
        {
            'type': 'cell',
            'criteria': '>',
            'value': 0,
            'format': error_format
        }
    )
    pass
def __export_bank():
    global excel_doc, bold, money, error_format, warning_format
    bank_sheet = excel_doc.add_worksheet("Bank Data")
    
    bank_data = bank_model.Bank.get_by_year(vc.active_year)
    
    # Adjust the column width.
    bank_sheet.set_column('A:B', 10)
    bank_sheet.set_column('D:G', 20)
    bank_sheet.set_column('I:J', 15)
    
    # Row Titles
    bank_sheet.write("B2", "Year", bold)
    bank_sheet.write("A3", "Bank Total", bold)
    bank_sheet.write("B3", "Cash Total", bold)
    
    bank_sheet.write("D3", "Account Cash Total", bold)
    bank_sheet.write("E3", "Account Check Total", bold)
    bank_sheet.write("F3", "Account Card Total", bold)
    bank_sheet.write("G3", "Account Scholar Total", bold)
    
    bank_sheet.write("I3", "Camper Total", bold)
    bank_sheet.write("J3", "Staff Total", bold)
    
    # Data
    bank_sheet.write("C2", bank_data.year, align_left)
    bank_sheet.write("A4", bank_data.bank_total, align_left)
    bank_sheet.write("B4", bank_data.cash_total, align_left)
    
    bank_sheet.write("D4", bank_data.account_cash_total, align_left)
    bank_sheet.write("E4", bank_data.account_check_total, align_left)
    bank_sheet.write("F4", bank_data.account_card_total, align_left)
    bank_sheet.write("G4", bank_data.account_scholar_total, align_left)
    
    bank_sheet.write("I4", bank_data.camper_total, align_left)
    bank_sheet.write("J4", bank_data.staff_total, align_left)
    pass
def __export_history():
    global excel_doc, bold, money, head_row, head_money, error_format, warning_format
    history_sheet = excel_doc.add_worksheet("Purchase History")
    
    purchases = history_model.History.get_all_reversed()
    
    # Adjust the column width.
    history_sheet.set_column('A:D', 30)
    
    # Row Titles
    history_sheet.write("A3", "Date & Time", bold)
    history_sheet.write("B3", "Customer Name", bold)
    history_sheet.write("C3", "Purchase Type(s)", bold)
    history_sheet.write("D3", "Items", bold)
    history_sheet.write("E3", "Sum Total", bold)
    
    row = 4
    total_donations = 0
    for purchase in purchases:
        history_sheet.write(f"A{row}", purchase.date_time)
        history_sheet.write(f"B{row}", purchase.customer_name)
        history_sheet.write(f"C{row}", purchase.purchase_type)
        history_sheet.write(f"D{row}", len(purchase.items))
        history_sheet.write(f"E{row}", purchase.sum_total, head_money)
        history_sheet.set_row(row-1, cell_format=head_row)
        row += 1
        
        for item in purchase.items:
            history_sheet.write(f"D{row}", item[0], align_left)
            history_sheet.write(f"E{row}", item[1], money)
            if item[0] == "Donation":
                total_donations += float(item[1][1:])
            row += 1
    
    history_sheet.write("D2", "Total Donations", bold)
    history_sheet.write("E2", total_donations, money)
    pass
