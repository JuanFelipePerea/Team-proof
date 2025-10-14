#Archivo main.py, principal

import functions

def show_menu():
    print(" -- Mini bind, beta proyect #1 --> Python json proof --\nOpciones")
    print("1. Crear nota")
    print("2. Ver todas las notas")
    print("3. Actualizar notas")
    print("4. Borrar nota")
    print("5. Buscar nota")
    print("6. Exportar notas")
    print("7. Importar notas")
    print("8. Salir")
    
def main():
    while True:
        show_menu()
        opcion = input("Selecciona una opcion: ").strip()
        if opcion == "1":
            functions.create_note()
        elif opcion == "2":
            functions.show_notes()
        elif opcion == "3":
            functions.update_note()
        elif opcion == "4":
            functions.del_note()
        elif opcion == "5":
            functions.search_notes()
        elif opcion == "6":
            functions.export_notes()
        elif opcion == "7":
            functions.import_notes()
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida")
        
main()