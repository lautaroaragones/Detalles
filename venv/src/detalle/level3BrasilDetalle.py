from tabulate import tabulate

#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        tipo = sheet.cell(row=row_index, column=8).value
        #Se verifica que el tipo no sea USG
        if(tipo != "USG"):
            # Se verifica que el tipo no sea RC
            if(tipo != "RC"):
                tarifa = str(sheet.cell(row=row_index, column=13).value)
                duracion = sheet.cell(row=row_index, column=10).value / 60
                #Se normalizan los numeros que empieza con . EJ .63
                tarifaConvertido = add_0_on_point(tarifa)
                total = (duracion * float(tarifaConvertido)) + total
            else:
                #Se suma la cabecera, es el tipo RC
                numerocionCabecera = sheet.cell(row=row_index,column=11).value
                total = total + float(numerocionCabecera)
    return total

# Se normalizan los numeros que empieza con . EJ .63
def add_0_on_point(numero):
    numero = str(numero)
    if (numero[:1].find(".") != -1):
        numeroConvertido = numero.replace(".", "0.")
    else:
        numeroConvertido = numero
    return numeroConvertido

#Se obtiene una lista de tipos
def get_lista_tipo(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        tipo = sheet.cell(row=row_index, column=8).value
        descripcion = sheet.cell(row=row_index, column=7).value
        if (tipo in list):
            list
        else:
            list.append(tipo)
    return list

#Se estandarizan los tipos de llamadas
def get_tipo_de_llamada_por_tipo(tipoLista):
    if(tipoLista == "Q"):
        return "0800"
    elif(tipoLista == "Y"):
        return "0800"
    elif(tipoLista == "RC"):
        return "Abono"
    elif(tipoLista == "R"):
        return "Local"
    elif(tipoLista == "USG"):
        return "Promedio"

#Se obtiene el total por cada descripcion
def get_total_por_tipo(sheet,lista):
    totalCosto = 0
    totalMinutos = 0
    listaTotal = []
    for indice_lista in range(0, (len(lista))):
        tipoLista = lista[indice_lista]
        for row_index in range(2, (sheet.max_row + 1)):
            tipo =sheet.cell(row=row_index, column=8).value
            if(tipo != "USG"):
                if(tipo == tipoLista):
                    if(tipo != "RC"):
                        tarifa = sheet.cell(row=row_index, column=13).value
                        tarifaConvertido = add_0_on_point(tarifa)
                        minutos = sheet.cell(row=row_index, column=10).value / 60
                        costo = float(tarifaConvertido) * minutos
                        totalCosto = float(costo) + totalCosto
                        totalMinutos = minutos + totalMinutos
                    elif(tipo == "RC"):
                        totalMinutos = 0
                        totalCosto = float(sheet.cell(row=row_index, column=11).value)
                descripcionTelefonia = get_tipo_de_llamada_por_tipo(tipoLista)
                if(validar_tipos_repetidos(listaTotal,descripcionTelefonia,totalMinutos,totalCosto)):
                    if(descripcionTelefonia != "Promedio"):
                        listaTotal.append([descripcionTelefonia, totalMinutos, totalCosto])
                totalCosto = 0
                totalMinutos = 0
    print(tabulate(listaTotal, headers=['Descripcion', 'Minutos' , 'Costo'], tablefmt='fancy_grid'))

#Se valida si la descripcion esta repetida en la lista, si lo esta se suman los minutos y el costo al existente
def validar_tipos_repetidos(listaTotal,descripcionTelefonia,totalMinutos,totalCosto):
    for indice_lista_total in range(0, (len(listaTotal))):
        if (listaTotal[indice_lista_total][0] != descripcionTelefonia):
            ""
        else:
            listaTotal[indice_lista_total][1] = listaTotal[indice_lista_total][1] + totalMinutos
            listaTotal[indice_lista_total][2] = listaTotal[indice_lista_total][2] + totalCosto
            return False
    return True