from tabulate import tabulate

from babel.numbers import format_currency

from bd import bdDetalle

#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = str(sheet.cell(row=row_index, column=11).value)
        descripcion = sheet.cell(row=row_index, column=7).value
        tipo = sheet.cell(row=row_index, column=8).value
        #Se verifica que la descripcion no sea el i800 Term (Es una descripcion interna de level 3)
        #Ademas de que no sea USG
        if( descripcion.find("i800 Term") == -1 and tipo != "USG"):
            #Se normalizan los numeros que empieza con . EJ .63
            costo = add_0_on_point(costo)
            total = float(costo) + total
    return format_currency(total, 'US', locale='en_US')


# Se normalizan los numeros que empieza con . EJ .63
def add_0_on_point(numero):
    numero = str(numero)
    if (numero[:1].find(".") != -1):
        numeroConvertido = numero.replace(".", "0.")
    else:
        #Se agrega el punto a los numeros que son 1.000 pero vienen como 1000 y sin 1,0
        if(len(numero) == 4 and numero.find(".") == -1):
            numero = list(numero)
            numero[1] = "."
            numero = "".join(numero)
        numeroConvertido = numero
    return numeroConvertido

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
            costo = add_0_on_point(sheet.cell(row=row_index, column=11).value)
            minutos = sheet.cell(row=row_index, column=10).value / 60
            if(descripcion == descripcionLista):
                totalCosto = float(costo) + totalCosto
                totalMinutos = minutos + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
            if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                if (descripcionTelefonia != "Non"):
                 listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

    # Se obtiene el total del consumo
    print("El total es: " + str(get_total(sheet)))

    # Se ingresan la inforamacion en la BD
    bdDetalle.getInformationBD(listaTotal, "USD", "Mexico", "CenturyLink")

#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista.find("i800 Term") != -1):
        return "Non"
    elif(descripcionLista.find("Mexico") != -1):
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