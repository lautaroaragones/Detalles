from tabulate import tabulate

from babel.numbers import format_currency

#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = str(sheet.cell(row=row_index, column=14).value)
        descripcion = sheet.cell(row=row_index, column=7).value
        tipo = sheet.cell(row=row_index, column=8).value
        #Se verifica que la descripcion no sea el i800 Term: Colombia (Es una descripcion interna de level 3)
        #Ademas de que no sea USG
        if( descripcion != "i800 Term: COLOMBIA " and tipo != "USG"):
            #Se normalizan los numeros que empieza con . EJ .63
            total = float(costo) + total
    return format_currency(total, 'CO', locale='es_CO')