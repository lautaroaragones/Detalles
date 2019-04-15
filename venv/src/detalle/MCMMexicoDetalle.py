from tabulate import tabulate
from babel.numbers import format_currency

#Obtiene el total de consumo
def get_total(sheet):
    totalCosto = 0
    costo = 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=12).value
        totalCosto = float(costo) + totalCosto
    return format_currency(totalCosto, 'BR', locale='pt_BR')