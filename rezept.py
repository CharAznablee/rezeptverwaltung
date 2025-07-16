def rezept_erstellen(name, zutaten_liste, zubereitung_liste):
    # Diese Funktion erstellt ein neues Rezept als Dictionary ( Wörterbuch )
    return {
        "name": name, # Der Name des Rezepts
        
        # Die Zutaten werden als liste von Dictionaries gespeichert.
        # Jeder Eintrag hat den schlüssel "name", un der Text wird vorher von Leerzeichen bereinigt
        "zutaten": [{"name": z.strip()} for z in zutaten_liste if z.strip()],
        
        # Die Zubereitung wird als Liste von Schritten gespeichert
        # Jeder Schritt hat eine Nummer ("Schritt") und den eigentlichen Text ("Zubereitung")
        "zubereitung": [{"schritt": i+1, "zubereitung": s.strip()} for i, s in enumerate(zubereitung_liste) if s.strip()]
    }