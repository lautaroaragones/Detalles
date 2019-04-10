import pyodbc
from pandas import DataFrame, ExcelWriter
import pandas
from tabulate import tabulate
from babel.numbers import format_currency

#Se convierte el Archvio MDB (Access) en un archivo de libro excel
def convertir_MDB_a_Excel(nombreExcel,query,path):
    # set up some constants
    MDB = path;
    DRV = '{Microsoft Access Driver (*.mdb)}';
    PWD = 'pw'

    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
    cur = con.cursor()

    # run a query and get the results
    SQL = query
    rows = cur.execute(SQL).fetchall()

    # Pandas reading values from SQL query, and building table
    sqlData = pandas.read_sql_query(SQL, con)

    # Pandas building dataframe, and exporting .xlsx copy of table
    df = DataFrame(data=sqlData)


    df.to_excel(''+nombreExcel+'.xlsx',
                header=True, index=False,sheet_name='default')
    dfHeaders = df.columns.values.tolist()
    dfHeadersArray = [dfHeaders]
    dfData = df.values.tolist()

    cur.close()
    con.close()

#Obtiene el total de consumo
def get_total(sheet):
    total= 0
    for row_index in range(2, (sheet.max_row + 1)):
        costo = sheet.cell(row=row_index, column=11).value
        total = float(costo) + total
    return format_currency(total, 'BR', locale='pt_BR')


#Se obtiene una lista de descripciones
def get_lista_descripcion(sheet):
    list = []
    for row_index in range(2, (sheet.max_row + 1)):
        descripcion = sheet.cell(row=row_index, column=8).value
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
            descripcion =sheet.cell(row=row_index, column=8).value
            costo = sheet.cell(row=row_index, column=11).value
            minutos = sheet.cell(row=row_index, column=9).value
            if(descripcion == descripcionLista):
                totalCosto = costo + totalCosto
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
    if(descripcionLista.find("CHAMADA LDI FIXO-FIXO") != -1):
        return "Internacional"
    elif(descripcionLista.find("CHAMADA LDI FIXO-MOVEL") != -1):
        return "Movil"
    elif(descripcionLista.find("CHAMADA LDN OFFNET FIXO-FIXO") != -1):
        return "LDN"
    elif(descripcionLista.find("CHAMADA LDN OFFNET FIXO-MOVEL") != -1):
        return "Movil"
    elif(descripcionLista.find("CHAMADA LDN PARA") != -1):
        return "0800 (Salientes)"
    elif(descripcionLista.find("CHAMADA LOCAL FIXO-FIXO") != -1):
        return "Local"
    elif(descripcionLista.find("CHAMADA LOCAL FIXO-MOVEL") != -1):
        return "Movil"
    elif(descripcionLista.find("CHAMADA LOCAL PARA") != -1):
        return "0800 (Salientes)"
    elif(descripcionLista.find("DDD") != -1):
        if(descripcionLista.find("DDD PARA TELEFONE FIXO") != -1):
            return "LDN"
        elif(descripcionLista.find("DDD PARA TELEFONE MOVEL") != -1):
            return "Movil"
        else:
            return "LDN"
    elif(descripcionLista.find("DDI") != -1):
        return "Internacional"
    elif(descripcionLista.find("SERVICO 0300") != -1):
        return "0800 (Salientes)"
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
    
    
