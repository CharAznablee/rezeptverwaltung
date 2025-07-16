import json # Zum Lesen und Schreiben von JSON-Dateien
import os   # Um zu prüfen, ob die Datei existiert

# Name der Datei, in der die Rezepte gespeichert werden
DATEINAME = "rezept.json"

def laden():
    # Wenn die Datei nicht existiert, gib eine Leere liste zurück
    if not os.path.exists(DATEINAME):
        return []
    
    # Datei im Lesemodus öffnen und Inhalte als JSON Laden
    with open(DATEINAME, "r", encoding="utf-8") as f:
        return json.load(f)
    
def speichern(rezepte):
    # Rezepte als JSON-Datei speichern
    # ensure_ascii=False sorgt dafür, dass Umlaut etc. korrekt gespeichert werden
    # indent=4 sorgt für eine lesbare Formatierung
    with open(DATEINAME, "w", encoding="utf-8") as f:
        json.dump(rezepte, f, ensure_ascii=False, indent=4)