# Rezeptverwaltungstool

Ein einfaches Python-Tool zur Verwaltung und Speicherung von Rezepten.

## Funktionen
- Neue Rezepte hinzufügen (Titel, Zutaten, Zubereitung)
- Rezepte anzeigen, bearbeiten und löschen
- Rezepte speichern und laden (JSON)
- grafische Benutzeroberfläche mit Qt
- Rezeptdetails werden beim Anklicken rechts im Layout angezeigt

## Projektstruktur
rezeptverwaltung/
    main.py # Startpunkt des Programms
    rezept.py # Klasse für einzelne Rezepte
    datenbank.py # Speichern und Laden der Rezepte
    gui.py # Grafische Benutzeroberfläche
    rezepte.json # Lokale Rezeptdatenbank
    README.md # Kurze beschreibung des Projekts
    LICENSE # Lizenzierung
    
## Zusatzfunktionen

Gespeicherte Rezepte werden in einer Tabelle angezeigt.  
Beim Anklicken eines vorhandenen Rezepts erscheinen die Details auf der rechten Seite des Layouts.

## Ziel

Dieses Projekt dient als Übung zur Projektstrukturierung, zur Dateiverwaltung und für erste GUI-Erfahrungen.  
Außerdem soll es helfen, sauberen Code zu schreiben und vorhandene Python-Skills zu verbessern.

## Anforderungen

- Python 3.x
- PyQt5

## Starten

```bash
python main.py

oder die main.py über ein IDE/Editor starten und ausführen

## ℹInfo

Die Nutzung und Weiterverarbeitung dieses Tools ist ausdrücklich erlaubt – auch die Umwandlung in eine `.exe`-Datei.  
Ich bitte lediglich darum, bei Weitergabe oder Veröffentlichung den ursprünglichen Autor zu nennen.

**Entwickelt von Rahat Mohammed (aka *Char Aznablee*)**
