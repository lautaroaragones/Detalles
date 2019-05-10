
import pymysql
import datetime
from entities import config_manager


def startDB():
    # Open database connection
    db = pymysql.connect("localhost","root","","regional" )

    return db

def closeDB(db):
    db.close()

def insertData(db,id_descripcion,id_moneda,id_pais,id_servicio,minutos,costo,date,name_avoxi = 'NULL'):
    date = convertDate(date)
    cursor = db.cursor()

    cursor.execute ("INSERT INTO consumo (id_descripcion,id_moneda,id_pais,id_servicio,minutos,name_avoxi,costo,date) VALUES ("+id_descripcion+","+id_moneda+","+id_pais+","+id_servicio+","+minutos+",'"+name_avoxi+"',"+costo+",%s)",date)

    db.commit()

def convertDate(date):
    return datetime.datetime.strptime(date, '%Y/%m')

def getInformationBD(listaTotal,moneda,pais,servicio):
    confirm = input("Desea guardar en la BD la informacion ? Y/N: ")
    if(confirm == "y" or confirm ==  "Y"):
        fechaBD = input("Ingrese la fecha del ciclo AAAA/MM (Por EJ: 2019/04): ")
        db = startDB()
        for indice_lista in range(0, (len(listaTotal))):
            #Avoxi se trata por separado, porque la descripcion es el pais donde se origino la llamada, por ende se guarda el nombre del pais en name_avoxi y su descripcion es Larga Distancia Internacional
            if(servicio != "Avoxi"):
                descripcionBD = str(config_manager.ConfigManager.get_value("descripcion", str(listaTotal[indice_lista][0])))
            else:
                descripcionBD = str(config_manager.ConfigManager.get_value("descripcion", "Larga Distancia Internacional"))
                nameAvoxiBD = str(listaTotal[indice_lista][0])
            monedaBD = str(config_manager.ConfigManager.get_value("moneda", str(moneda)))
            paisBD = str(config_manager.ConfigManager.get_value("paises", str(pais)))
            servicioBD = str(config_manager.ConfigManager.get_value("servicio", str(servicio)))
            costoBD = str(listaTotal[indice_lista][1])
            minutosBD = str(listaTotal[indice_lista][2])
            if (servicio != "Avoxi"):
                if(validateDescription(db, str(listaTotal[indice_lista][0]))):
                    insertData(db, descripcionBD, monedaBD, paisBD, servicioBD, costoBD, minutosBD, fechaBD)
            else:
                insertData(db, descripcionBD, monedaBD, paisBD, servicioBD, costoBD, minutosBD, fechaBD,nameAvoxiBD)
        closeDB(db)
        print("Guardado realizado con exito")
    else:
        print("No se guardo en la BD")

def validateDescription(db,descripcion):
    db = pymysql.connect("localhost", "root", "", "regional")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM descripcion WHERE nombre_descripcion = '"+str(descripcion)+"'")

    if(cursor.rowcount == 0):
        return False
    else:
        return True


