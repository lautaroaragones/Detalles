from tabulate import tabulate
from bd import bdDetalle

#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = str(sheet.cell(row=row_index, column=13).value)
        tipo = sheet.cell(row=row_index, column=8).value
        #Se verifica que el tipo sea USG
        if( tipo == "USG"):
            #Se normalizan los numeros que empieza con . EJ .63
            costoConvertido = add_0_on_point(costo)
            total = float(costoConvertido) + total
    #Se agrega el abono al final (120)
    return total + 120


# Se normalizan los numeros que empieza con . EJ .63
def add_0_on_point(numero):
    numero = str(numero)
    if (numero[:1].find(".") != -1):
        numeroConvertido = numero.replace(".", "0.")
    else:
        numeroConvertido = numero
    return numeroConvertido

#Se obtiene una lista de descripciones
def get_lista_descripcion(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        tipo = sheet.cell(row=row_index, column=8).value
        if (tipo == "USG"):
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
    #Se agrega el abono Hardcodeado
    listaTotal.append(["Abono", 1, 120])
    for indice_lista in range(0, (len(lista))):
        descripcionLista = lista[indice_lista]
        for row_index in range(2, (sheet.max_row + 1)):
            descripcion =sheet.cell(row=row_index, column=7).value
            costo = sheet.cell(row=row_index, column=13).value
            minutos = sheet.cell(row=row_index, column=10).value
            if(descripcion == descripcionLista):
                costoConvertido = add_0_on_point(costo)
                totalCosto = float(costoConvertido) + totalCosto
                totalMinutos = minutos + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
            if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

    # Se obtiene el total del consumo
    print("El total es: " + str(get_total(sheet)))

    # Se ingresan la inforamacion en la BD
    bdDetalle.getInformationBD(listaTotal, "PEN", "Peru", "CenturyLink")


#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista == "0800 National Incoming calls **RW"):
        return "0800"
    elif(descripcionLista == "International Calls **RW"):
        return "Larga Distancia Internacional"
    elif(descripcionLista == "Local Calls **RW"):
        return "Local"
    elif(descripcionLista == "Local Incoming Calls to 0800 **RW"):
        return "0800"
    elif(descripcionLista == "National calls **RW"):
        return "Larga Distancia Nacional"
    elif(descripcionLista == "Peru - Moviles Calls **RW"):
        return "Celulares"
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