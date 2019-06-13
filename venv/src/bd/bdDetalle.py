
import pymysql
import datetime
from entities import config_manager


#Inicia la Base de Datos
def startDB():
    # Open database connection
    db = pymysql.connect("localhost","root","","regional" )

    return db

#Cierra la conexion con la Base de Datos
def closeDB(db):
    db.close()

#Inserta la query en la base de datos
def insertData(db,id_descripcion,id_moneda,id_pais,id_servicio,minutos,costo,date,name_avoxi = 'NULL'):
    date = convertDate(date)
    cursor = db.cursor()

    cursor.execute ("INSERT INTO consumo (id_descripcion,id_moneda,id_pais,id_servicio,minutos,name_avoxi,costo,date) VALUES ("+id_descripcion+","+id_moneda+","+id_pais+","+id_servicio+","+minutos+",'"+name_avoxi+"',"+costo+",%s)",date)

    db.commit()

#Cambia el costo y los minutos de una row repetida
def changeRowRepeated(db, paisBD, servicioBD,minutosBD, costoBD, descripcionBD, fechaBD,name_avoxi = 'NULL'):
    date = convertDate(fechaBD)
    cursor = db.cursor()

    cursor.execute ("UPDATE consumo SET costo = "+costoBD+", minutos = "+minutosBD+" WHERE id_pais = "+paisBD+" AND id_servicio = "+servicioBD+" AND id_pais = "+paisBD+" AND name_avoxi = '"+name_avoxi+"' AND id_descripcion = "+descripcionBD+" AND date = %s",date)

    db.commit()

#Inserta o updatea datos masivamente
def insertRows(db,listaTotal,pais,servicio, moneda,fechaBD,tipo):
    for indice_lista in range(0, (len(listaTotal))):
        # Avoxi se trata por separado, porque la descripcion es el pais donde se origino la llamada, por ende se guarda el nombre del pais en name_avoxi y su descripcion es Larga Distancia Internacional
        if (servicio != "Avoxi"):
            descripcionBD = str(config_manager.ConfigManager.get_value("descripcion", str(listaTotal[indice_lista][0])))
        else:
            descripcionBD = str(config_manager.ConfigManager.get_value("descripcion", "Larga Distancia Internacional"))
            nameAvoxiBD = str(listaTotal[indice_lista][0])
        monedaBD = str(config_manager.ConfigManager.get_value("moneda", str(moneda)))
        paisBD = str(config_manager.ConfigManager.get_value("paises", str(pais)))
        servicioBD = str(config_manager.ConfigManager.get_value("servicio", str(servicio)))
        minutosBD = str(listaTotal[indice_lista][1])
        costoBD = str(listaTotal[indice_lista][2])
        if (servicio != "Avoxi"):
            if (validateDescription(db, str(listaTotal[indice_lista][0]))):
                if(tipo=="Insert"):
                    insertData(db, descripcionBD, monedaBD, paisBD, servicioBD, minutosBD, costoBD, fechaBD)
                if (tipo == "Update"):
                    changeRowRepeated(db, paisBD, servicioBD, minutosBD, costoBD, descripcionBD, fechaBD)
        else:
            if (tipo == "Insert"):
                insertData(db, descripcionBD, monedaBD, paisBD, servicioBD, minutosBD, costoBD, fechaBD, nameAvoxiBD)
            if (tipo == "Update"):
                changeRowRepeated(db, paisBD, servicioBD, minutosBD, costoBD, descripcionBD, fechaBD, nameAvoxiBD)

#Convierte el string date en un datetime
def convertDate(date):
    return datetime.datetime.strptime(date, '%Y/%m')

#Obtiene la informacion para insertar en la BD (Metodo que se conecta con exterior)
def getInformationBD(listaTotal,moneda,pais,servicio):
    confirm = input("Desea guardar en la BD la informacion ? Y/N: ")
    if(confirm == "y" or confirm ==  "Y"):
        fechaBD = input("Ingrese la fecha del ciclo AAAA/MM (Por EJ: 2019/04): ")
        db = startDB()
        #Si no tiene niguna row repetida, lo inserta
        if(validateRepeatedField(db, pais, servicio, fechaBD)):
            tipo = "Insert"
            insertRows(db, listaTotal, pais, servicio, moneda, fechaBD , tipo)
            print("Guardado realizado con exito")
        #Si encuentra una row repetida valida si queres updatear los datos
        else:
            print('\n' * 1)
            print("El registro que usted quiere ingresar ya fue ingresado con anterioridad")
            confirmUpdate = input("¿Quiere cambiar los valores viejos por los valores actuales? Y/N: ")
            if(confirmUpdate == "y" or confirmUpdate == "Y"):
                tipo = "Update"
                insertRows(db, listaTotal, pais, servicio, moneda, fechaBD, tipo)
                print('\n' * 1)
                print("Se genero el UPDATE exitosamente !")
            else:
                print('\n' * 1)
                print("No se genero el UPDATE")
        closeDB(db)
    else:
        print("No se guardo en la BD")

#Valida que la descripicion este en la tabla descripcion
def validateDescription(db,descripcion):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM descripcion WHERE nombre_descripcion = '"+str(descripcion)+"'")

    if(cursor.rowcount == 0):
        return False
    else:
        return True

#Valida si una row esta repetida
def validateRepeatedField(db,idPais,idServicio,fecha):
    cursor = db.cursor()
    date = convertDate(fecha)
    cursor.execute("SELECT id_consumo FROM consumo AS C INNER JOIN pais AS P ON C.id_pais = P.id_pais INNER JOIN servicio AS S ON S.id_servicio = C.id_servicio WHERE P.nombre_pais = '"+str(idPais)+"' AND S.nombre_servicio = '"+str(idServicio)+"' AND C.date = %s",date)

    if(cursor.rowcount == 0):
        return True
    else:
        return False

