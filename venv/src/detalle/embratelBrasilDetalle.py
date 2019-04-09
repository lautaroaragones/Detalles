import pyodbc
from pandas import DataFrame, ExcelWriter
import pandas

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
    
    
