import os
import glob

from detalle import avoxiDetalle , level3PeruDetalle, level3ArgentinaDetalle, level3BrasilDetalle, level3ColombiaDetalle,level3MexicoDetalle,level3ChileDetalle , embratelBrasilDetalle
from excel import excelDetalle

from pyexcel.cookbook import merge_all_to_a_book



def menu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    print('\n' * 1)
    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Avoxi")
    print("\t2 - Level 3 - Peru")
    print("\t3 - Level 3 - Argentina")
    print("\t4 - Level 3 - Brasil")
    print("\t5 - Level 3 - Colombia")
    print("\t6 - Level 3 - Mexico")
    print("\t7 - Level 3 - Chile")
    print("\t8 - Embratel - Brasil")
    print("\t9 - Salir")

def option_menu():
    while True:
        # Mostramos el menu
        menu()

        # solicituamos una opción al usuario
        opcionMenu = input("Inserta un numero valor >> ")

        if opcionMenu == "1":
            print("")
            menu_avoxi()
            input()
        elif opcionMenu == "2":
            print("")
            nombre = "PERU"
            subtotal = level3PeruDetalle.get_total_por_descripcion
            lista = level3PeruDetalle.get_lista_descripcion
            total = level3PeruDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input()
        elif opcionMenu == "3":
            print("")
            nombre = "ARGENTINA"
            subtotal = level3ArgentinaDetalle.get_total_por_descripcion
            lista = level3ArgentinaDetalle.get_lista_descripcion
            total = level3ArgentinaDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input("")
        elif opcionMenu == "4":
            print("")
            nombre = "BRASIL"
            subtotal = level3BrasilDetalle.get_total_por_tipo
            lista = level3BrasilDetalle.get_lista_tipo
            total = level3BrasilDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input("")
        elif opcionMenu == "5":
            print("")
            nombre = "COLOMBIA"
            subtotal = level3ColombiaDetalle.get_total_por_descripcion
            lista = level3ColombiaDetalle.get_lista_descripcion
            total = level3ColombiaDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input("")
        elif opcionMenu == "6":
            print("")
            nombre = "MEXICO"
            subtotal = level3MexicoDetalle.get_total_por_descripcion
            lista = level3MexicoDetalle.get_lista_descripcion
            total = level3MexicoDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input("")
        elif opcionMenu == "7":
            print("")
            nombre = "CHILE"
            subtotal = level3ChileDetalle.get_total_por_descripcion
            lista = level3ChileDetalle.get_lista_descripcion
            total = level3ChileDetalle.get_total
            menu_level3(nombre, subtotal, lista, total)
            input("")
        elif opcionMenu == "8":
            print("")
            menu_embratel_brasil()
            input("")
        elif opcionMenu == "9":
            break
        else:
            print("")
            input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")

def menu_avoxi():
    print("--- USTED ELEGIO AVOXI ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .CSV")
    print("Columnas a seleccionar cuando se baja el detalle: Fecha/Hora | Numero/ext/troncalSIP | Pais | Numero (DE) | Numero (A) | Duracion | Costo\n")
    getPath = input("Inserta el path (Debe incluir el nombre del archivo) >> ")
    path = getPath.replace('"', '')

    #Se convierte el .csv a .xlsx (Se cachea el archivo)
    merge_all_to_a_book(glob.glob(path), "avoxi.xlsx")

    # Se obtiene el excel - Detalle Avoxi
    excel_avoxi = excelDetalle.open_excel("avoxi.xlsx")
    # Se obtiene la sheet de la tabla - Detalle Avoxi
    sheet_tabla_avoxi = excelDetalle.open_sheet_by_name(excel_avoxi, 'call-logs.csv')

    # Se obtiene la tabla por paises
    avoxiDetalle.get_total_por_pais(sheet_tabla_avoxi,avoxiDetalle.get_lista_paises(sheet_tabla_avoxi))
    # Se obtiene el total del consumo
    print("El total es: " + str(avoxiDetalle.get_total(sheet_tabla_avoxi)))
    os.remove('avoxi.xlsx')


def menu_level3(nombre,subtotal,lista,total):
    print("--- USTED ELEGIO LEVEL 3 - "+ nombre +" ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .XLSX\n")
    getPath = input("Inserta el path (Debe incluir el nombre del archivo) >> ")
    path = getPath.replace('"', '')

    # Se obtiene el excel - Detalle Level 3 Peru
    excel_level3 = excelDetalle.open_excel(path)
    # Se obtiene la sheet de la tabla - Level 3 Peru
    sheet_tabla_level3 = excelDetalle.open_sheet_default(excel_level3)

    #Se obtiene la tabla por descripciones
    subtotal(sheet_tabla_level3,lista(sheet_tabla_level3))
    #Se obtiene el total del consumo
    print("El total es: " + str(total(sheet_tabla_level3)))

def menu_embratel_brasil():
    print("--- USTED ELEGIO - EMBRATEL BRASIL ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .MDB\n")
    getPath = input("Inserta el path 0800 (Debe incluir el nombre del archivo) >> ")
    path0800 = getPath.replace('"', '')

    getPath = input("Inserta el path Salientes (Debe incluir el nombre del archivo) >> ")
    pathSalientes = getPath.replace('"', '')

    query = "SELECT * FROM chamadas"
    
    embratelBrasilDetalle.convertir_MDB_a_Excel('0800',query,path0800)
    embratelBrasilDetalle.convertir_MDB_a_Excel('salientes', query, pathSalientes)
    
    # Se obtiene el excel - Detalle Embratel 0800
    excel_0800 = excelDetalle.open_excel('0800.xlsx')
    # Se obtiene la sheet de la tabla - Embratel 0800
    sheet_tabla_0800 = excelDetalle.open_sheet_default(excel_0800)

    # Se obtiene el excel - Detalle Embratel Salientes
    excel_salientes = excelDetalle.open_excel('salientes.xlsx')
    # Se obtiene la sheet de la tabla - Embratel Salientes
    sheet_tabla_salientes = excelDetalle.open_sheet_default(excel_salientes)

    embratelBrasilDetalle.get_total_por_descripcion(sheet_tabla_salientes,embratelBrasilDetalle.get_lista_descripcion(sheet_tabla_salientes))

    print("El total de salientes es: " + str(embratelBrasilDetalle.get_total(sheet_tabla_salientes)))
    print("El total de 0800 es: " + str(embratelBrasilDetalle.get_total(sheet_tabla_0800)))