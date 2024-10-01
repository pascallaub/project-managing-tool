projekte = []

def neues_projekt():
    projekt_name = input("Projektname: ")
    projekt_start = input("Startdatum: ")
    projekt_prio = input("Priorität: ")
    projekte.append({'Projektname': projekt_name, 'Startdatum': projekt_start, 'Priorität': projekt_prio})

def projekt_anzeigen():
    print(projekte)

def projekt_bearbeiten():
    pass

def projekt_del():
    pass

def neue_aufgabe():
    pass

def aufgaben_anzeigen():
    pass

def aufgabe_bearbeiten():
    pass

def aufgabe_del():
    pass

def aufgabe_sort():
    pass

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
            if auswahl_menu == '2':
                projekt_anzeigen()
                continue
            elif auswahl_menu == '11':
                beenden()
        except ValueError:
            print("Falsche Eingabe!")

menu()