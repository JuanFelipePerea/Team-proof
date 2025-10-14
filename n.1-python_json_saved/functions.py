#Archivo functions.py

import os
import json

# Obtener la ruta absoluta del directorio actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "notes.json")

# Es un sistema de CRUD

# CREATE --------------------------------------------------------------------------

def load_notes():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent = 4)

def create_note():
    print("\n-- Crear nueva nota --")
    title = input("Titulo: ")
    description = input("Descripcion: ")
    date = input("Fecha (YYYY-MM-DD): ")
    state = input("Estado (pendiente / en progreso / completado): ")
    
    notes = load_notes()
    new_ID = 1 if not notes else max(note["id"] for note in notes) + 1
    
    new_note = {
        "id": new_ID,
        "title": title,
        "description": description,
        "date": date,
        "state": state,
    }
    notes.append(new_note)
    save_notes(notes)
    print("Nota guardada con exito!")
    
    
# READ --------------------------------------------------------------------------

def show_notes():
    notes = load_notes()
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
        
    
# UPDATE --------------------------------------------------------------------------

def update_note():
    notes = load_notes()
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
    new_title = input("Ingresa un nuevo titulo (Deja vacio para no cambiar): ").strip()
    if new_title:
        note['title'] = new_title
        
    print(f"Descripcion actual: {note['description']}")
    new_description = input("Ingresa una nueva descripcion (Deja vacio para no cambiar): ").strip()
    if new_description:
        note['description'] = new_description  
        
    print(f"Fecha actual: {note['date']}")
    new_date = input("Ingresa una nueva fecha (Deja vacio para no cambiar): ").strip()
    if new_date:
        note['date'] = new_date  
        
    print(f"Estado actual: {note['state']}")
    new_state = input("Ingresa un nuevo estado (Deja vacio para no cambiar): ").strip()
    if new_state:
        note['state'] = new_state  
        
    save_notes(notes)
    print("Nota actualizada con éxito.")
    
# DELETE --------------------------------------------------------------------------

def del_note():
    notes = load_notes()
    if not notes:
        print("No hay ninguna nota para borrar")
        return
    
    try:
        ID_note = int(input("Ingresa el ID de la nota que vas a borrar: "))
    except ValueError:
        print("ID invalido")
        return
    
    note = next((n for n in notes if n["id"] == ID_note), None)
    if not note:
        print("Nota no encontrada")
        return  
    
    confirm = input(f"Estas seguro que quieres borrar la nota con ID {ID_note}? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Operacion cancelada.")
        return
    notes.remove(note)
    save_notes(notes)
    print("Nota borrada con éxito.")
    
# SEARCH --------------------------------------------------------------------------

def search_notes():
    notes = load_notes()
    if not notes:
        print("No hay ninguna nota para buscar")
        return
    
    keyword = input("Ingresa una palabra clave para buscar en titulos y descripciones: ").strip().casefold()
    if not keyword:
        print("Palabra clave vacia")
        return
    
    found_notes = [note for note in notes if keyword in note["title"].lower() or keyword in note["description"].lower()]
    
    if not found_notes:
        print("No se encontraron notas que coincidan con la palabra clave.")
        return
    
    print(f"\nNotas encontradas con la palabra clave '{keyword}':\n-----\n")
    for note in found_notes:
        print(f"\nID: {note['id']}")
        print(f"Titulo: {note['title']}")
        print(f"Descripcion: {note['description']}")
        print(f"Fecha: {note['date']}")
        print(f"Estado: {note['state']}\n\n-----\n")
        
# EXPORT --------------------------------------------------------------------------

def export_notes():
    notes = load_notes()
    if not notes:
        print("No hay ninguna nota para exportar")
        return
    
    export_file = input("Ingresa el nombre del archivo de exportacion (sin extension): ").strip()
    
    if not export_file:
        print("Nombre de archivo invalido")
        return
    
    export_path = os.path.join(BASE_DIR, f"{export_file}.json")
        
    if os.path.exists(export_path):
        confirm = input(f"Archivo {export_path} creado. ¿Deseas sobreescribirlo? (Y/N): ").strip().lower()
        if confirm != 'y':
            print("Operacion cancelada.")
            return
        
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)
        
    print(f"Notas exportadas con exito a {export_path}")
    
# IMPORT --------------------------------------------------------------------------
def import_notes():
    import_file = input("Ingresa el nombre del archivo a importar (sin extension): ").strip()
    
    if not import_file:
        print("Nombre de archivo invalido")
        return
    
    import_path = os.path.join(BASE_DIR, f"{import_file}.json")
    
    if not os.path.exists(import_path):
        print(f"Archivo {import_path} no encontrado.")
        return
    
    with open(import_path, "r", encoding="utf-8") as f:
        try:
            imported_notes = json.load(f)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON. Asegurate de que el formato sea correcto.")
            return
    
    if not isinstance(imported_notes, list) or not all(isinstance(note, dict) for note in imported_notes):
        print("El formato del archivo importado es incorrecto. Debe ser una lista de notas.")
        return
    
    notes = load_notes()
    existing_ids = {note["id"] for note in notes}
    next_id = max(existing_ids, default=0) + 1
    
    for note in imported_notes:
        if not all(key in note for key in ("title", "description", "date", "state")):
            print("Una o mas notas en el archivo importado tienen un formato incorrecto y seran omitidas.")
            continue
        
        note["id"] = next_id
        next_id += 1
        notes.append(note)
    
    save_notes(notes)
    print(f"Notas importadas con exito desde {import_path}")