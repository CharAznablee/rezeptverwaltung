from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
                             QMessageBox, QListWidget, QListWidgetItem, QHBoxLayout)
import datenbank # Modul für das Laden und Speichern der Rezepte
import rezept    # Modul für die Rezeptlogik (z.B. rezepte_erstellen Funktion)

class Rezeptverwaltung(QWidget):
    def __init__(self):
        super().__init__()
        # Fenster-Titel und Größe festlegen
        self.setWindowTitle("Manuelles Eingabetool")
        self.setGeometry(100, 100, 500, 500)
        
        layout = QVBoxLayout() # Haupt-Layout vertikal
        
        # Label und Eingabefeld für den Gerichtnamen
        self.name_label = QLabel("Gerichtname: ")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        # Label und Textfeld für Zutaten (mehrzeilig)
        """ Untereinander eingeben Bitte 
            Zutaten am besten in dem Format schreiben 
            (z.B. Zucker 50 gramm
                  Milch 250 ml usw. )"""
        self.zutaten_label = QLabel("Zutaten (eine pro Zeile): ")
        layout.addWidget(self.zutaten_label)
        self.zutaten_input = QTextEdit()
        layout.addWidget(self.zutaten_input)
        
        # Label und Textfeld für die Zubereitungs schritte (mehrzeilig)
        """ Genau wie bei den Zutaten untereinander eingeben"""
        self.zubereitung_label = QLabel("Zubereitung (eine pro Zeile): ")
        layout.addWidget(self.zubereitung_label)
        self.zubereitung_input = QTextEdit()
        layout.addWidget(self.zubereitung_input)
        
        # Button zum Speichern des Rezeptes, mit Klick-event verbunden
        self.save_button = QPushButton("Rezept Speichern")
        self.save_button.clicked.connect(self.speichern)
        layout.addWidget(self.save_button)
        
        # Button zum Anzeigen aller Rezepte
        self.show_button = QPushButton("Rezepte anzeigen")
        self.show_button.clicked.connect(self.rezepte_anzeigen)
        layout.addWidget(self.show_button)       
        
        self.setLayout(layout) # Layout setzen
        
    def speichern(self):
        # Werte aus den Eingabefeldern auslesen und Whitespace entfernen
        name = self.name_input.text().strip()
        zutaten_text = self.zutaten_input.toPlainText().strip()
        zubereitung_text = self.zubereitung_input.toPlainText().strip()
        
        # überprüfen, ob alle Felder ausgefüllt sind
        if not name or not zutaten_text or not zubereitung_text:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen!")
            return       
        
        # Bestehende Rezepte laden
        rezepte = datenbank.laden()
        # Neues Rezept erstellen mit Liste der Zutaten und Zubereitunsschritte
        neues_rezept = rezept.rezept_erstellen(
            name,
            zutaten_text.splitlines(), # Jede zeile als einzelnes Element
            zubereitung_text.splitlines()
        )
        rezepte.append(neues_rezept) # Neues Rezept hinzufügen
        datenbank.speichern(rezepte) # Rezepte speichern
            
        # Info-Meldung anzeigen, Eingabefelder leeren
        QMessageBox.information(self, "Gespeichert", f"Rezept '{name} wurde gespeichert!")
        self.name_input.clear()
        self.zutaten_input.clear()
        self.zubereitung_input.clear()
    
    def rezepte_anzeigen(self):
        # Rezepte laden
        rezepte = datenbank.laden()
        if not rezepte:
            # Falls keine Rezepte vorhanden, Info anzeigen und abbrechen
            QMessageBox.information(self, "Keine Rezepte", "Es wurden noch keine Rezepte gespeichert.")
            return
        
        # Neues Fenster öffnen, um die Rezepte anzuzeigen (Parent None = eigenes Fenster)
        self.anzeige_fenster = RezeptAnzeigeFenster(rezepte, None)
        self.anzeige_fenster.show()
    
class RezeptAnzeigeFenster(QWidget):
    def __init__(self, rezepte, parent=None):
        super().__init__(parent)
        # Fenster-Titel und Größe
        self.setWindowTitle("Rezeptübersicht")
        self.setGeometry(200, 200, 600, 400)
        
        self.rezepte = rezepte # Liste der Rezepte
        
        main_layout = QHBoxLayout() # Haupt-Layout horizontal
        
        # Links: Liste aller Rezeptnamen als klickbare Liste
        self.rezept_liste = QListWidget()
        for ein_rezept in self.rezepte:
            item = QListWidgetItem(ein_rezept["name"]) # Rezeptname als Listeneintrag
            self.rezept_liste.addItem(item)
        self.rezept_liste.currentRowChanged.connect(self.rezept_auswaehlen) # Event, wenn ein Rezept ausgewaählt wird
        
        main_layout.addWidget(self.rezept_liste)
        
        # Rechts: Anzeige der Rezeptdetails und Buttons
        detail_layout = QVBoxLayout()
        
        self.detail_label = QLabel("Wählen ein Rezept aus der Liste")
        self.detail_label.setWordWrap(True) # Zeilenumbruch aktivieren
        detail_layout.addWidget(self.detail_label)
        
        # Button zum Löschen des ausgewählten Rezepts
        self.loeschen_button = QPushButton("Rezept Löschen")
        self.loeschen_button.clicked.connect(self.rezept_loeschen)
        self.loeschen_button.setEnabled(False) # Anfangs deaktiviert
        detail_layout.addWidget(self.loeschen_button)
        
        # Button zum bearbeiten des ausgewählten Rezepts
        self.show_button = QPushButton("Rezept Bearbeiten")
        self.show_button.clicked.connect(self.rezept_bearbeiten)
        self.show_button.setEnabled(False) # Anfangs deaktiviert
        detail_layout.addWidget(self.show_button)
        
        main_layout.addLayout(detail_layout)
        
        self.setLayout(main_layout)
        self.show()
        
    def rezept_auswaehlen(self, index):
        # Wenn kein Rezept ausgewählt wurde (index -1), Text zurücksetzen und Buttons deaktivieren
        if index == -1:
            self.detail_label.setText("Wähle ein Rezept aus der Liste")
            self.loeschen_button.setEnabled(False)
            self.show_button.setEnabled(False)
            return
            
        rezept = self.rezepte[index]
        
        # Rezeptdetails zusammenbauen als Text
        details = f"{rezept['name']}\n\nZutaten:\n"
        for z in rezept["zutaten"]:
            if isinstance(z, dict) and "name" in z:
                details += f" - {z['name']}\n"
            else:
                details += f" - {z}\n"
                
        details += "\nZubereitung:\n"
        for i, s in enumerate(rezept["zubereitung"], start=1):
            if isinstance(s, dict) and "zubereitung" in s:
                details += f" {i}. {s['zubereitung']}\n"
            else:
                details += f" {i}. {s}\n"
          
        # Details im label anzeigen
        self.detail_label.setText(details)
        # Buttons aktivieren
        self.loeschen_button.setEnabled(True)
        self.show_button.setEnabled(True)
            
    def rezept_loeschen(self):
        index = self.rezept_liste.currentRow()
        if index == -1:
            return
            
        name = self.rezepte[index]["name"]
        # Sicherheitsabfrage, ob Rezept wirklich gelöscht werden soll
        bestätigen = QMessageBox.question(self, "Rezept Löschen", f"Möchtest du das Rezept '{name}' wirklich löschen ?", QMessageBox.Yes | QMessageBox.No)
        
        if bestätigen == QMessageBox.Yes:
            del self.rezepte[index] # Rezept aus Liste löschen
            QMessageBox.information(self, "Gelöscht", f"'{name}' wurde gelöscht.")
            self.rezept_liste.takeItem(index) # Eintrag aus der GUI-Liste entfernen
            self.detail_label.setText("Wähle ein Rezept aus der Liste.")
            self.loeschen_button.setEnabled(False)
            self.show_button.setEnabled(False)
            
            datenbank.speichern(self.rezepte) # Geänderte Liste speichern
                      
    def rezept_bearbeiten(self):
        index = self.rezept_liste.currentRow()
        if index == -1:
            return
            
        rezept = self.rezepte[index]
            
        # Fenster zum Bearbeiten des ausgewählten Rezeptes öffnen
        self.bearbeiten_fenster = RezeptBearbeitenFenster(rezept, index, self)
        self.bearbeiten_fenster.show()

    def update_rezept(self, index, neues_rezept):
        # Rezept in der Liste aktualisieren
        self.rezepte[index] = neues_rezept
        # Namen in der Liste aktualisieren
        self.rezept_liste.item(index).setText(neues_rezept["name"])
        datenbank.speichern(self.rezepte) # Speichern
        self.rezept_auswaehlen(index) # Details anzeigen aktualisieren

        
class RezeptBearbeitenFenster(QWidget):
    def __init__(self, rezept, index, anzeige_fenster):
        super().__init__()
        self.rezept = rezept
        self.index = index
        self.anzeige_fenster = anzeige_fenster # Referenz auf das Anzeige-Fenster
        
        self.setWindowTitle(f"Rezept bearbeiten: {rezept['name']}")
        self.setGeometry(250, 250, 500, 400)
        
        layout = QVBoxLayout()
        
        # Eingabe für den Namen
        layout.addWidget(QLabel("Gerichtname:"))
        self.edit_name = QLineEdit(rezept["name"])
        layout.addWidget(self.edit_name)
        
        # Eingabe für Zutaten als mehrzeiliger Text (eine Zutat pro Zeile)
        layout.addWidget(QLabel("Zutaten (eine pro Zeile):"))
        # Zutaten in Text umwandeln (falls Dict, dann "name" extrahieren)
        zutaten_text = "\n".join([z if isinstance(z, str) else z.get("name", "") for z in rezept["zutaten"]])
        self.edit_zutaten = QTextEdit(zutaten_text)
        layout.addWidget(self.edit_zutaten)
        
        # Eingabe für Zubereitung (eine Pro Zeile)
        layout.addWidget(QLabel("Zubereitung (eine pro Zeile):"))
        # Zubereitungsschritte in Text umwandeln (falls Dict, dann "zubereitung" extrahieren)
        zubereitung_text = "\n".join([s if isinstance(s, str) else s.get("zubereitung", "") for s in rezept["zubereitung"]])
        self.edit_zubereitung = QTextEdit(zubereitung_text)
        layout.addWidget(self.edit_zubereitung)
        
        # Button zum Speichern der Änderungen
        save_button = QPushButton("Änderung speichern")
        save_button.clicked.connect(self.speichern)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
        
    def speichern(self):
        # Werte aus den Eingabefeldern auslesen
        name = self.edit_name.text().strip()
        zutaten = [line.strip() for line in self.edit_zutaten.toPlainText().splitlines() if line.strip()]
        zubereitung = [line.strip() for line in self.edit_zubereitung.toPlainText().splitlines() if line.strip()]
        
        # Überprüfen, ob alle Felder ausgefüllt sind
        if not name or not zutaten or not zubereitung:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen!")
            return
        
        # Neues Rezept-Dictionary erstellen, Zutaten und Zubereitung als Liste von Dicts
        neues_rezept = {
            "name": name,
            "zutaten": [{"name": z} for z in zutaten],
            "zubereitung": [{"zubereitung": s} for s in zubereitung]
        }
        
        # Rezept im Anzeige-Fenster aktualisieren
        self.anzeige_fenster.update_rezept(self.index, neues_rezept)
        QMessageBox.information(self, "Gespeichert", f"Rezept '{name}' wurde gespeichert.")
        self.close() # Fenster Schließen