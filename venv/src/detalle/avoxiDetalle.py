from tabulate import tabulate
from bd import bdDetalle


#Obtiene el total de consumo por cada pais
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
            total = sheet.cell(row=row_index, column=7).value + total
    return total

def get_lista_paises(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        pais = sheet.cell(row=row_index, column=3).value
        if (pais in list):
            list
        else:
            list.append(pais)
    return list

def get_total_por_pais(sheet,lista):
    totalCosto = 0
    totalMinutos = 0
    listaTotal = []
    for indice_lista in range(0, (len(lista))):
        paisLista = lista[indice_lista]
        for row_index in range(2, (sheet.max_row + 1)):
            pais =sheet.cell(row=row_index, column=3).value
            costo = sheet.cell(row=row_index, column=7).value
            minutos = convert_horas_en_minutos(sheet.cell(row=row_index, column=6).value)

            if(pais == paisLista and costo != 0):
                totalCosto = costo + totalCosto
                totalMinutos = minutos + totalMinutos
        if(totalCosto != 0 and totalMinutos != 0):
            listaTotal.append([paisLista,totalMinutos,totalCosto])
        totalCosto = 0
        totalMinutos = 0
    print(tabulate(listaTotal, headers=['Pais','Minutos','Costo'], tablefmt='fancy_grid'))

    #Se obtiene el total del consumo
    print("El total es: " + str(get_total(sheet)))

    #Se ingresan la inforamacion en la BD
    bdDetalle.getInformationBD(listaTotal, "USD", "Multi Pais", "Avoxi")

def convert_horas_en_minutos(horas):
    if(horas == None):
        return 0
    return horas/60