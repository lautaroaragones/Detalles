import os
import glob

from detalle import avoxiDetalle , level3PeruDetalle, level3ArgentinaDetalle, level3BrasilDetalle
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
            menu_level3_peru()
            input()
        elif opcionMenu == "3":
            print("")
            menu_level3_argentina()
            input("")
        elif opcionMenu == "4":
            print("")
            menu_level3_brasil()
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

def menu_level3_peru():
    print("--- USTED ELEGIO LEVEL 3 - PERU ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .XLSX\n")
    getPath = input("Inserta el path (Debe incluir el nombre del archivo) >> ")
    path = getPath.replace('"', '')


    # Se obtiene el excel - Detalle Level 3 Peru
    excel_level3_peru = excelDetalle.open_excel(path)
    # Se obtiene la sheet de la tabla - Level 3 Peru
    sheet_tabla_level3_peru = excelDetalle.open_sheet_default(excel_level3_peru)

    #Se obtiene la tabla por descripciones
    level3PeruDetalle.get_total_por_descripcion(sheet_tabla_level3_peru, level3PeruDetalle.get_lista_descripcion(sheet_tabla_level3_peru))
    #Se obtiene el total del consumo
    print("El total es: " + str(level3PeruDetalle.get_total(sheet_tabla_level3_peru)))

def menu_level3_argentina():
    print("--- USTED ELEGIO LEVEL 3 - ARGENTINA ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .XLSX\n")
    getPath = input("Inserta el path (Debe incluir el nombre del archivo) >> ")
    path = getPath.replace('"', '')


    # Se obtiene el excel - Detalle Level 3 Peru
    excel_level3_argentina = excelDetalle.open_excel(path)
    # Se obtiene la sheet de la tabla - Level 3 Peru
    sheet_tabla_level3_argentina = excelDetalle.open_sheet_default(excel_level3_argentina)

    #Se obtiene la tabla por descripciones
    level3ArgentinaDetalle.get_total_por_descripcion(sheet_tabla_level3_argentina, level3ArgentinaDetalle.get_lista_descripcion(sheet_tabla_level3_argentina))
    #Se obtiene el total del consumo
    print("El total es: " + str(level3ArgentinaDetalle.get_total(sheet_tabla_level3_argentina)))

def menu_level3_brasil():
    print("--- USTED ELEGIO LEVEL 3 - BRASIL ---")
    print("EL ARCHIVO DEBE ESTAR EN FORMATO .XLSX\n")
    getPath = input("Inserta el path (Debe incluir el nombre del archivo) >> ")
    path = getPath.replace('"', '')


    # Se obtiene el excel - Detalle Level 3 Peru
    excel_level3_brasil = excelDetalle.open_excel(path)
    # Se obtiene la sheet de la tabla - Level 3 Peru
    sheet_tabla_level3_brasil = excelDetalle.open_sheet_default(excel_level3_brasil)

    #Se obtiene la tabla por descripciones
    level3BrasilDetalle.get_total_por_tipo(sheet_tabla_level3_brasil, level3BrasilDetalle.get_lista_tipo(sheet_tabla_level3_brasil))
    #Se obtiene el total del consumo
    print("El total es: " + str(level3BrasilDetalle.get_total(sheet_tabla_level3_brasil)))

