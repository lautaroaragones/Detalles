from datetime import time
from tabulate import tabulate
from babel.numbers import format_currency

from bd import bdDetalle


#Obtiene el total de consumo
def get_total(sheet,coeficienteEntrante,coeficienteSaliente):
    totalCosto = 0
    netAmount = 0
    for row_index in range(1, (sheet.max_row + 1)):
        descripcion = sheet.cell(row=row_index, column=11).value
        grossAmount = sheet.cell(row=row_index, column=7).value / 100
        #Verifica que sea 0800 o no, porque el coeficiente varia
        netAmount = get_net_amount(descripcion,coeficienteEntrante,coeficienteSaliente,grossAmount)
        totalCosto = float(netAmount) + totalCosto
    return format_currency(totalCosto, 'BR', locale='pt_BR')

def get_net_amount(descripcion,coeficienteEntrante,coeficienteSaliente,grossAmount):
    # Verifica que sea 0800 o no, porque el coeficiente varia
    if (descripcion == "Serviço de Rede"):
        return grossAmount * coeficienteEntrante
    else:
        return grossAmount * coeficienteSaliente

#Se obtiene el coeficiente de las llamadas entrantes
def get_coeficiente_entrante(total_entrante,sheet):
    total_costo = 0
    for row_index in range(1, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=7).value / 100
        descripcion = sheet.cell(row=row_index, column=11).value
        #Se verifica que sea 0800
        if( descripcion == "Serviço de Rede"):
            total_costo = float(costo) + total_costo
    return float(total_entrante)/total_costo

#Se obtiene el coeficiente de las llamadas salientes
def get_coeficiente_saliente(total_saliente,sheet):
    total_costo = 0
    for row_index in range(1, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=7).value / 100
        descripcion = sheet.cell(row=row_index, column=11).value
        #Se verifica que no sea 0800
        if( descripcion != "Serviço de Rede"):
            total_costo = float(costo) + total_costo
    return float(total_saliente)/total_costo

#Se obtiene una lista de descripciones
def get_lista_descripcion(sheet):
    list = []
    for row_index in range(1, (sheet.max_row + 1)):
        descripcion = sheet.cell(row=row_index, column=11).value
        if (descripcion in list):
            list
        else:
            list.append(descripcion)
    return list

#Se obtiene el total por cada descripcion
def get_total_por_descripcion(sheet,lista,coeficienteEntrante,coeficienteSaliente):
    totalCosto = 0
    totalMinutos = 0
    listaTotal = []
    for indice_lista in range(0, (len(lista))):
        descripcionLista = lista[indice_lista]
        for row_index in range(1, (sheet.max_row + 1)):
            descripcion =sheet.cell(row=row_index, column=11).value
            grossAmount = sheet.cell(row=row_index, column=7).value / 100
            # Verifica que sea 0800 o no, porque el coeficiente varia
            netAmount = get_net_amount(descripcionLista, coeficienteEntrante, coeficienteSaliente,grossAmount)
            minutos = sheet.cell(row=row_index, column=8).value
            if(descripcion == descripcionLista):
                totalCosto = float(netAmount) + totalCosto
                #Se redondean los minutos
                totalMinutos = redondeo_minutos(minutos) + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
            if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

    #Se obtiene el total del consumo
    print("El total es: " + str(get_total(sheet,coeficienteEntrante,coeficienteSaliente)))

    #Se ingresan la inforamacion en la BD
    bdDetalle.getInformationBD(listaTotal, "BRL", "Brasil", "Intelig")


#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista == "Serviço de Rede"):
        return "0800"
    elif(descripcionLista == "Local p/ Fixo"):
        return "Local"
    elif(descripcionLista == "A Cobrar Local de Móvel"):
        return "Celulares"
    elif(descripcionLista == "Dentro do Estado p Fixo"):
        return "Local"
    elif(descripcionLista == "Dentro do Estado p Móvel"):
        return "Celulares"
    elif(descripcionLista == "Entre Estados p Móvel"):
        return "Celulares"
    elif(descripcionLista == "Local p/ Móvel"):
        return "Celulares"
    elif(descripcionLista == "Local p/ Móvel - Especial"):
        return "Celulares"
    elif(descripcionLista == "Entre Estados p Fixo"):
        return "Larga Distancia Nacional"
    elif(descripcionLista == "A Cobrar Local de Fixo"):
        return "Local"
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

#Se redondean los minutos
def redondeo_minutos(tiempo):
    if (tiempo.second > 30):
        return tiempo.minute + 1
    else:
        return tiempo.minute
