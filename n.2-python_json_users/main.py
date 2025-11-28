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
    username = input("\nIngresa tu usuario ya existente o registra uno nuevo: ").strip().lower()
    print(f"Bienvenido, {username}!\n")
    
    while True:
        show_menu()
        opcion = input("Selecciona una opcion: ").strip()
        if opcion == "1":
            functions.create_note(username)
        elif opcion == "2":
            functions.show_notes(username)
        elif opcion == "3":
            functions.update_note(username)
        elif opcion == "4":
            functions.del_note(username)
        elif opcion == "5":
            functions.search_notes(username)
        elif opcion == "6":
            functions.export_notes(username)
        elif opcion == "7":
            functions.import_notes(username)
        elif opcion == "8":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida")

main()