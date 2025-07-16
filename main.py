# Hauptdatei für das Rezeptverwaltungstool

import sys # Ermöglicht Zugriff auf Systemfunktionen (z.B. Programm beenden)
from PyQt5.QtWidgets import QApplication # Die Hauptklasse für alle PyQt-Anwendungen
from gui import Rezeptverwaltung # Importiert das Haupt-Gui-Fenster aus der gui.py

# Prüft, ob das Skript direkt ausgeführt wird (nicht importiert)
if __name__ == "__main__":
    app = QApplication(sys.argv) # erstellt die Qt-Anwendung
    fenster = Rezeptverwaltung() # erstellt das Hauptfenster der Anwendung
    fenster.show() # Zeigt das Fenster an
    sys.exit(app.exec_()) # Starte die Qt-Ereignisschleife und beendet das Programm korrekt beim beenden
