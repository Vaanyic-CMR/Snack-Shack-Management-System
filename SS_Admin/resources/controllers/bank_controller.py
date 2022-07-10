from ..models import (
    bank
)
from .. import var_const as vc
from .. import server

def handle_bank_command( data ):
    print( f"[COMMAND] Branch: 'bank' | {data}" )
    
    if data[0] == "api/bank/cash":
        b = bank.Bank.get_by_year(vc.active_year)
        b.bank_total += data[1]
        b.cash_total += data[1]
        bank.Bank.save(b.to_dict())
        return server.SUCCESS_MSG
    if data[0] == "api/bank/donation":
        b = bank.Bank.get_by_year(vc.active_year)
        b.donation_total += data[1]
        bank.Bank.save(b.to_dict())
        return server.SUCCESS_MSG
    if data[0] == "api/bank/eow_return":
        b = bank.Bank.get_by_year(vc.active_year)
        b.bank_total -= data[1]
        b.cash_total -= data[1]
        bank.Bank.save(b.to_dict())
        return server.SUCCESS_MSG
    