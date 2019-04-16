from tabulate import tabulate
from babel.numbers import format_currency

#Obtiene el total de consumo
def get_total(sheet):
    totalCosto = 0
    costo = 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=12).value
        totalCosto = float(costo) + totalCosto
    return format_currency(totalCosto, 'MX', locale='es_MX')

#Se obtiene una lista de descripciones
def get_lista_descripcion(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        descripcion = sheet.cell(row=row_index, column=3).value
        if (descripcion in list):
            list
        else:
            list.append(descripcion)
    return list

#Se obtiene el total por cada descripcion
def get_total_por_descripcion(sheet,lista):
    totalCosto = 0
    totalMinutos = 0
    listaTotal = []
    for indice_lista in range(0, (len(lista))):
        descripcionLista = lista[indice_lista]
        for row_index in range(2, (sheet.max_row + 1)):
            descripcion =sheet.cell(row=row_index, column=3).value
            costo = sheet.cell(row=row_index, column=12).value
            minutos = sheet.cell(row=row_index, column=9).value
            if(descripcion == descripcionLista):
                totalCosto = float(costo) + totalCosto
                totalMinutos = minutos + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
            if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                 listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista.find("Local") != -1):
        return "Local"
    elif(descripcionLista.find("800-LD") != -1):
        return "0800"
    elif(descripcionLista == "Celular"):
        return "Movil"
    elif(descripcionLista == "LD Internacional"):
        return "Internacional"
    elif(descripcionLista == "LD Nacional"):
        return "LDN"
    elif(descripcionLista == "LDN-CEL"):
        return "Movil"
    return descripcionLista


#Se valida si la descripcion esta repetida en la lista, si lo esta se suman los minutos y el costo al existente
def validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto):
    for indice_lista_total in range(0, (len(listaTotal))):
        if (listaTotal[indice_lista_total][0] != descripcionTelefonia):
            ""
        else:
            listaTotal[indice_lista_total][1] = listaTotal[indice_lista_total][1] + totalMinutos
            listaTotal[indice_lista_total][2] = listaTotal[indice_lista_total][2] + totalCosto
            return False
    return True