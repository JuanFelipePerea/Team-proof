# functions.py

import os
import json

# Ruta base para guardar archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(BASE_DIR, "users")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

# Cargar notas de un usuario
def load_notes(username):
    user_file = os.path.join(USERS_DIR, f"{username}_notes.json")
    if not os.path.exists(user_file):
        return []
    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)

# Guardar notas de un usuario
def save_notes(notes, username):
    user_file = os.path.join(USERS_DIR, f"{username}_notes.json")
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)

# CREATE
def create_note(username):
    print("\n-- Crear nueva nota --")
    title = input("Titulo: ")
    description = input("Descripcion: ")
    date = input("Fecha (YYYY-MM-DD): ")
    state = input("Estado (pendiente / en progreso / completado): ")

    notes = load_notes(username)
    new_ID = 1 if not notes else max(note["id"] for note in notes) + 1

    new_note = {
        "id": new_ID,
        "title": title,
        "description": description,
        "date": date,
        "state": state,
    }
    notes.append(new_note)
    save_notes(notes, username)
    print("Nota guardada con éxito!")

# READ
def show_notes(username):
    notes = load_notes(username)
    if not notes:
        print("No hay ninguna nota guardada")
        return

    print("\nTodas las notas:\n-----\n")
    for note in notes:
        print(f"\nID: {note['id']}")
        print(f"Titulo: {note['title']}")
        print(f"Descripcion: {note['description']}")
        print(f"Fecha: {note['date']}")
        print(f"Estado: {note['state']}\n\n-----\n")

# UPDATE
def update_note(username):
    notes = load_notes(username)
    if not notes:
        print("No hay ninguna nota para actualizar")
        return

    try:
        ID_note = int(input("Ingresa el ID de la nota que vas a actualizar: "))
    except ValueError:
        print("ID invalido")
        return
    
    note = next((n for n in notes if n["id"] == ID_note), None)
    if not note:
        print("Nota no encontrada")
        return
    
    print(f"Titulo actual: {note['title']}")
    new_title = input("Nuevo titulo (deja vacío para no cambiar): ").strip()
    if new_title:
        note['title'] = new_title
        
    print(f"Descripcion actual: {note['description']}")
    new_description = input("Nueva descripcion: ").strip()
    if new_description:
        note['description'] = new_description
        
    print(f"Fecha actual: {note['date']}")
    new_date = input("Nueva fecha: ").strip()
    if new_date:
        note['date'] = new_date
        
    print(f"Estado actual: {note['state']}")
    new_state = input("Nuevo estado: ").strip()
    if new_state:
        note['state'] = new_state
        
    save_notes(notes, username)
    print("Nota actualizada con éxito.")
    
# DELETE
def del_note(username):
    notes = load_notes(username)
    if not notes:
        print("No hay ninguna nota para borrar")
        return
    
    try:
        ID_note = int(input("ID de la nota a borrar: "))
    except ValueError:
        print("ID invalido")
        return
    
    note = next((n for n in notes if n["id"] == ID_note), None)
    if not note:
        print("Nota no encontrada")
        return
    
    confirm = input(f"¿Seguro que deseas borrar la nota con ID {ID_note}? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Operacion cancelada.")
        return
    
    notes.remove(note)
    save_notes(notes, username)
    print("Nota borrada con éxito.")

# SEARCH
def search_notes(username):
    notes = load_notes(username)
    if not notes:
        print("No hay notas para buscar")
        return

    keyword = input("Palabra clave: ").strip().casefold()
    if not keyword:
        print("Palabra clave vacía")
        return

    found_notes = [note for note in notes if keyword in note["title"].lower() or keyword in note["description"].lower()]
    if not found_notes:
        print("No se encontraron notas que coincidan.")
        return

    print(f"\nNotas encontradas con '{keyword}':\n-----\n")
    for note in found_notes:
        print(f"\nID: {note['id']}")
        print(f"Titulo: {note['title']}")
        print(f"Descripcion: {note['description']}")
        print(f"Fecha: {note['date']}")
        print(f"Estado: {note['state']}\n\n-----\n")

# EXPORT
def export_notes(username):
    notes = load_notes(username)
    if not notes:
        print("No hay notas para exportar")
        return

    export_file = input("Nombre del archivo de exportación (sin extensión): ").strip()
    if not export_file:
        print("Nombre inválido")
        return

    export_path = os.path.join(EXPORT_DIR, f"{export_file}.json")
    if os.path.exists(export_path):
        confirm = input(f"Archivo {export_path} existe. ¿Sobrescribir? (Y/N): ").strip().lower()
        if confirm != 'y':
            print("Operación cancelada.")
            return

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)

    print(f"Notas exportadas con éxito a {export_path}")

# IMPORT
def import_notes(username):
    import_file = input("Archivo a importar (sin extensión): ").strip()
    if not import_file:
        print("Nombre inválido")
        return

    import_path = os.path.join(EXPORT_DIR, f"{import_file}.json")
    if not os.path.exists(import_path):
        print("Archivo no encontrado.")
        return

    with open(import_path, "r", encoding="utf-8") as f:
        try:
            imported_notes = json.load(f)
        except json.JSONDecodeError:
            print("Archivo JSON inválido.")
            return

    if not isinstance(imported_notes, list) or not all(isinstance(note, dict) for note in imported_notes):
        print("Formato de archivo incorrecto.")
        return

    notes = load_notes(username)
    existing_ids = {note["id"] for note in notes}
    next_id = max(existing_ids, default=0) + 1

    for note in imported_notes:
        if not all(key in note for key in ("title", "description", "date", "state")):
            print("Una o más notas tienen formato incorrecto. Serán omitidas.")
            continue

        note["id"] = next_id
        next_id += 1
        notes.append(note)

    save_notes(notes, username)
    print(f"Notas importadas con éxito desde {import_path}")
