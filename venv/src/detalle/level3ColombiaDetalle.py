from tabulate import tabulate

from babel.numbers import format_currency
from bd import bdDetalle
from entities import config_manager

#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = str(sheet.cell(row=row_index, column=13).value)
        descripcion = sheet.cell(row=row_index, column=7).value
        tipo = sheet.cell(row=row_index, column=8).value
        #Se verifica que la descripcion no sea el i800 Term: Colombia (Es una descripcion interna de level 3)
        #Ademas de que no sea USG
        if( descripcion != "i800 Term: COLOMBIA " and tipo != "USG"):
            #Se normalizan los numeros que empieza con . EJ .63
            total = float(costo) + total
    return format_currency(total, 'CO', locale='es_CO')

#Se obtiene una lista de descripciones
def get_lista_descripcion(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        tipo = sheet.cell(row=row_index, column=8).value
        descripcion = sheet.cell(row=row_index, column=7).value
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
            descripcion =sheet.cell(row=row_index, column=7).value
            costo = sheet.cell(row=row_index, column=13).value
            minutos = sheet.cell(row=row_index, column=10).value / 60
            if(descripcion == descripcionLista):
                totalCosto = costo + totalCosto
                totalMinutos = minutos + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
            if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                if (descripcionTelefonia != "Non"):
                 listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
        totalCosto = 0
        totalMinutos = 0

    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

    #Se obtiene el total del consumo
    print("El total es: " + str(get_total(sheet)))

    #Se ingresan la inforamacion en la BD
    bdDetalle.getInformationBD(listaTotal, "COP", "Colombia", "CenturyLink")

#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista == "i800 Term: COLOMBIA"):
        return "Non"
    elif(descripcionLista == "Colombia - Abonado Ordinario"):
        return "0800"
    elif(descripcionLista == "Colombia - Abonado Movil"):
        return "0800"
    elif(descripcionLista == "International Calls **RW"):
        return "Non"
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