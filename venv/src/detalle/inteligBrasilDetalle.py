

def get_coeficiente_entrante(total_entrante,sheet):
    total_costo = 0
    for row_index in range(1, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=7).value / 100
        descripcion = sheet.cell(row=row_index, column=11).value
        if( descripcion == "Serviço de Rede"):
            #Se normalizan los numeros que empieza con . EJ .63
            total_costo = float(costo) + total_costo
    return float(total_entrante)/total_costo

def get_coeficiente_saliente(total_saliente,sheet):
    total_costo = 0
    for row_index in range(1, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=7).value / 100
        descripcion = sheet.cell(row=row_index, column=11).value
        if( descripcion != "Serviço de Rede"):
            #Se normalizan los numeros que empieza con . EJ .63
            total_costo = float(costo) + total_costo
    return float(total_saliente)/total_costo