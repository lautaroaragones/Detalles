import openpyxl
import menuDetalle

#Abre un excel
def open_excel(path):
    try:
        print("---Se inicia la API de Excel---")
        excelfile = openpyxl.load_workbook(path)  # Se abre el excel con extension xsls
        print("---Excel iniciado con exito path: "+path+"---")
        return excelfile
    except IOError:
        print("\nPor favor, elija un excel correcto")
        menuDetalle.option_menu()
    except openpyxl.utils.exceptions.InvalidFileException:
        print("\nFormato del excel invalido, debe ser un .xlsx")
        menuDetalle.option_menu()

#Abre la sheet de un excel con nombre
def open_sheet_by_name(excelfile,nombre_sheet):
    try:
        print("Se inicia el excel: " + nombre_sheet + "")
        sheet1 = excelfile.get_sheet_by_name(nombre_sheet)  # Se obtiene la sheet correspondiente
        return sheet1
    except AttributeError:
        print("Por favor, elija una sheet correcta")
        return menuDetalle.option_menu()
    except KeyError:
        print("Por favor, elija una sheet correcta")
        return menuDetalle.option_menu()

def open_sheet_default(excelfile):
    try:
        print("Se inicia el excel la sheet por default")
        sheet1 = excelfile.get_active_sheet()
        return sheet1
    except AttributeError:
        print("Por favor, elija una sheet correcta")
        return menuDetalle.option_menu()