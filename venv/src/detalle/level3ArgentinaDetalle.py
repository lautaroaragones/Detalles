from tabulate import tabulate

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
    return total


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
    list.append("Moviles")
    return list


#Se obtiene el total por cada descripcion
def get_total_por_descripcion(sheet,lista):
    """
    Se inician las variables
    """
    totalCosto = 0
    totalMinutos = 0
    totalCostoMovil = 0
    totalMinutosMovil = 0
    totalCostoI0800 = 0
    totalMinutosI0800 = 0
    listaTotal = []
    """
    Inicia el ciclo por cada item de la lista
    """
    for indice_lista in range(0, (len(lista))):
        descripcionLista = lista[indice_lista]
        """
        Inicia el ciclo por cada item del excel
        """
        for row_index in range(2, (sheet.max_row + 1)):
            """
            Se obtienen los valores del excel
            """
            descripcion = sheet.cell(row=row_index, column=7).value
            costo = sheet.cell(row=row_index, column=13).value
            minutos = sheet.cell(row=row_index, column=10).value
            """
            Se compara si la descripcion de la lista es igual a la descripcion del excel
            """
            if(descripcion == descripcionLista):
                #Se convierte el costo por problemas de .05
                costoConvertido = add_0_on_point(costo)
                # Se suman los valores totales
                totalCosto = float(costoConvertido) + totalCosto
                totalMinutos = minutos + totalMinutos
                """
                Se valida si en nacionales o locales la llamada es movil
                """
                if (validar_moviles(float(minutos), float(costoConvertido), descripcion)):
                    #Se resta del total el importe anteriormente sumado
                    totalCosto = totalCosto - float(costoConvertido)
                    totalMinutos = totalMinutos - minutos
                    #Se suman a las variables globales de Movil
                    totalCostoMovil = totalCostoMovil + float(costoConvertido)
                    totalMinutosMovil = totalMinutosMovil + minutos
                """
                Se valida si en Internacional es un 0800 (Problema de los 690.. 0800 de USA)
                """
                if (validar_0800_int(float(minutos), float(costoConvertido), descripcion)):
                    # Se resta del total el importe anteriormente sumado
                    totalCosto = totalCosto - float(costoConvertido)
                    totalMinutos = totalMinutos - minutos
                    # Se suman a las variables globales de Movil
                    totalCostoI0800 = totalCostoI0800 + float(costoConvertido)
                    totalMinutosI0800 = totalMinutosI0800 + minutos
         #Se obtiene la descripcion personalizada EJ: 0800
        descripcionTelefonia = get_tipo_de_llamada_por_descripcion(descripcionLista)
        """
         Se valida que no este repetida en la lista la descripcion
         """
        if(validar_descripciones_repetidas(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
            #Se utliza esta validacion para que no ingresen el movil como lista en 0 0
            if (totalCosto != 0 and totalMinutos != 0):
                if(descripcionTelefonia != "0800"):
                    listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
                else:
                    #Se agregan los minutos del I800 (690... 0800 de USA)
                    listaTotal.append([descripcionTelefonia, totalMinutos + totalMinutosI0800, totalCosto + totalCostoI0800])

        """
         Se valida si la descripcion es movil
         """
        if(descripcionTelefonia == "Moviles"):
            #Se agrega a la lista el Movil, y se le agregan las variables globales de moviles
            listaTotal.append([descripcionTelefonia, totalMinutosMovil, totalCostoMovil])
        #Se resetean las variables a 0 despues de finalizar cada corrida
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))




#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_descripcion(descripcionLista):
    if(descripcionLista == "0810 National Incoming calls **RW"):
        return "0800"
    elif(descripcionLista == "International Calls **RW"):
        return "Internacional"
    elif(descripcionLista == "Local Calls **RW"):
        return "Locales"
    elif(descripcionLista == "Local Incoming Calls to 0810 **RW"):
        return "0800"
    elif(descripcionLista == "National calls **RW"):
        return "Nacional"
    elif(descripcionLista == "Calls to toll free **RW"):
        return "Locales"
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

#Se valida si la llamada nacional o local es movil
def validar_moviles(totalMinutos,totalCosto, descripcion):
    if(totalCosto/totalMinutos > 0.8 and descripcion == "Calls to toll free **RW"):
        return True
    if(totalCosto/totalMinutos > 0.8 and descripcion == "National calls **RW"):
        return True
    if(totalCosto/totalMinutos > 0.8 and descripcion == "Local Calls **RW"):
        return True
    return False

#Se valida que el tipo de llamada es un 690... (Llamada 0800 de USA)
def validar_0800_int(totalMinutos,totalCosto, descripcion):
    if (totalCosto / totalMinutos < 1 and descripcion == "International Calls **RW"):
        return True
    return False