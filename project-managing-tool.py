from datetime import datetime

projekte = []
aufgaben = []


def neues_projekt():
    projekt_name = input("Projektname: ")
    projekt_start = input("Startdatum: ")
    projekt_prio = input("Priorität: ")
    projekte.append({'Projektname': projekt_name, 'Startdatum': projekt_start, 'Priorität': projekt_prio, 'Aufgaben': aufgaben})

def projekt_anzeigen():
    print(projekte)

def projekt_bearbeiten():
    suche = input("Gib den Projektnamen ein: ")
    ergebnis = list(filter(lambda projekt: projekt["Projektname"] == suche, projekte))

    if not ergebnis:
        print("Projekt nicht gefunden!")
        return
    
    projekt = ergebnis[0]       #Gibt nur das erste Projekt aus bei mehreren
    aendern = input(f"Möchtest du dieses {ergebnis} ändern? j/n: ").lower()

    if aendern == 'j':
        neuer_name = input("Neuer Projektname: ")
        projekt['Projektname'] = neuer_name
        print("Projektname geändert!")
    else:
        print("Keine Änderung vorgenommen!")


def projekt_del():
    suche = input("Gib den Projektnamen ein: ")
    ergebnis = list(filter(lambda projekt: projekt["Projektname"] == suche, projekte))
        
    if not ergebnis:
        print("Projekt nicht gefunden!")
        return
        
    projekt = ergebnis[0]
    delete = input(f"Möchtest du dieses {ergebnis} löschen? j/n: ").lower()
    if delete == 'j':
        projekte.remove(projekt)
        print(f"Das Projekt {ergebnis} wurde gelöscht!")
    else:
        print("Löschen abgebrochen!")


def neue_aufgabe():
    aufgabe = input("Welchem Projekt möchtest du eine Aufgabe hinzufügen? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Projekt gefunden!")
        return
    
    projekt = ergebnis[0]
    korrekt = input(f"Möchtest du diesem Projekt {projekt} Aufgaben hinzufügen? j/n: ").lower()
    if korrekt == 'j':
        titel = input("Wie ist der Titel der Aufgabe? ")
        beschreibnung = input("Beschreibe die Aufgabe: ")
        datum = input("Fälligkeitsdatum: ")
        status = input("Status: ")
        projekt['Aufgaben'].append({'Titel': titel, 'Beschreibung': beschreibnung, 'Datum': datum, 'Status': status})
        print("Aufgaben zum Projekt hinzugefügt!")
    else:
        print("Abgebrochen!")


def aufgaben_anzeigen():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du anzeigen? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Projekt gefunden!")
        return

    projekt = ergebnis[0]
    print(projekt['Aufgaben'])

def aufgabe_bearbeiten():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du bearbeiten? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Projekt gefunden!")
        return
    
    projekt = ergebnis[0]
    korrekt = input(f"Möchtest du die Aufgaben dieses Projekts {projekt} ändern? j/n: ").lower()
    if korrekt == 'j':
        aufgaben_alt = input("Welche Aufgabe möchtest du bearbeiten? ")
        aufgaben_suche = list(filter(lambda aufgabe: aufgabe['Titel'] == aufgaben_alt, projekt['Aufgaben']))

        if not aufgaben_suche:
            print("Keine Aufgabe gefunden!")
            return
        
        aufgabe_ergebnis = aufgaben_suche[0]
        check = input(f"Möchtest du diese Aufgabe {aufgabe_ergebnis} bearbeiten? j/n: ").lower()
        if check == 'j':
            neuer_titel = input("Gib den neuen Titel der Aufgabe ein: ")
            neue_beschreibung = input("Gib eine neue Beschreibung ein: ")
            neues_datum = input("Gib ein neues Datum ein: ")
            neuer_status = input("Gib einen neuen Status ein (offen, in bearbeitung, verschoben, erledigt): ")
            index = next(i for i, aufgabe in enumerate(projekt['Aufgaben']) if aufgabe['Titel'] == aufgaben_alt)
            projekt['Aufgaben'][index] = {'Titel': neuer_titel, 'Beschreibung': neue_beschreibung, 'Datum': neues_datum, 'Status': neuer_status}
            print("Bearbeitete Aufgabe zum Projekt hinzugefügt!")
        else:
            print("Aufgabe nicht gefunden!")

    else:
        print("Vorgang abgebrochen!")


def aufgabe_del():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du löschen? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Projekt gefunden!")
        return
    
    projekt = ergebnis[0]
    korrekt = input(f"Ist dies {projekt} das richtige Projekt? j/n: ").lower()
    if korrekt == 'j':
        alle = input("Möchtest du alle Aufgaben löschen? j/n: ").lower()
        if alle == 'j':
            projekt['Aufgaben'].clear()
            print("Alle Aufgaben gelöscht!")
        else:
            print(projekt['Aufgaben'])
            welche = input("Welche Aufgaben möchtest du löschen? Tippe hier: ")
            aufgaben_suche = list(filter(lambda aufgabe: aufgabe['Titel'] == welche, projekt['Aufgaben']))

        if not aufgaben_suche:
            print("Keine Aufgabe gefunden!")
            return
        
        aufgabe_ergebnis = aufgaben_suche[0]
        check = input(f"Möchtest du diese Aufgabe {aufgabe_ergebnis} löschen? j/n: ").lower()
        if check == 'j':
            index = next(i for i, aufgabe in enumerate(projekt['Aufgaben']) if aufgabe['Titel'] == welche)
            projekt['Aufgaben'][index].clear()
            print("Aufgabe gelöscht!")
            
        else:
            print("Vorgang beendet!")
    else:
        print("Vorgang beendet!")

def aufgabe_sort():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du sortieren? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Projekt gefunden!")
        return
    
    projekt = ergebnis[0]
    korrekt = input(f"Ist dies {projekt} das richtige Projekt? j/n: ").lower()
    if korrekt == 'j':
        ordnung = input("Möchtest du nach Datum oder Status sortieren? d/s: ").lower()
        if ordnung == 'd':
            ordnung_datum = sorted(projekt['Aufgaben'], key=lambda aufgabe: datetime.strptime(aufgabe['Datum'], '%d.%m.%Y'))
            print(ordnung_datum)
        elif ordnung == 's':
            ordnung_status = sorted(projekt['Aufgaben'], key=lambda aufgabe: aufgabe['Status'])
            print(ordnung_status)
        else:
            print("Falsche Eingabe!")

def aufgabe_erledigt():
    pass

def beenden():
    quit()

def menu():
    while True:
        auswahl_menu = input("1. Neues Projekt erstellen\n2. Projekte anzeigen\n3. Projekt bearbeiten\n4. Projekt löschen\n5. Neue Aufgabe zu einem Projekt hinzufügen\n6. Aufgaben anzeigen\n7. Aufgabe bearbeiten\n8. Aufgabe löschen\n9. Aufgaben sortieren\n10. Aufgabe als erledigt markieren\n11. Programm beenden\nTippe eine Zahl ein: ")
        try:
            if auswahl_menu == '1':
                neues_projekt()
                continue
            elif auswahl_menu == '2':
                projekt_anzeigen()
                continue
            elif auswahl_menu == '3':
                projekt_bearbeiten()
                continue
            elif auswahl_menu == '4':
                projekt_del()
                continue
            elif auswahl_menu == '5':
                neue_aufgabe()
                continue
            elif auswahl_menu == '6':
                aufgaben_anzeigen()
                continue
            elif auswahl_menu == '7':
                aufgabe_bearbeiten()
                continue
            elif auswahl_menu == '8':
                aufgabe_del()
                continue
            elif auswahl_menu == '9':
                aufgabe_sort()
                continue
            elif auswahl_menu == '10':
                aufgabe_erledigt()
                continue
            elif auswahl_menu == '11':
                beenden()
        except ValueError:
            print("Falsche Eingabe!")

menu()