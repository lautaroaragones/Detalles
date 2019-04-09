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
    
    
