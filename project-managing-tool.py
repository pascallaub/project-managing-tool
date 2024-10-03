from datetime import datetime
import json
import sqlite3
import os

def database_connection():
    return sqlite3.connect("ProjekteDB/projects.db")
    
aufgaben = []

def neues_projekt():
    projekte = database_connection()
    cursor = projekte.cursor()
    projekt_name = input("Projektname: ")
    projekt_start = input("Startdatum: ")
    projekt_prio = input("Priorität: ")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projekte (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   projektname TEXT NOT NULL,
                   startdatum DATE,
                   prioritaet TEXT
        )
    ''')
    cursor.execute("INSERT INTO projekte (projektname, startdatum, prioritaet) VALUES(?,?,?)", (projekt_name, projekt_start, projekt_prio))
    projekte.commit()
    print("Projekt hinzugefügt!")
    projekte.close()

def projekt_anzeigen():
    projekte = database_connection()
    cursor = projekte.cursor()
    cursor.execute("SELECT * FROM projekte")
    inhalt = cursor.fetchall()
    print(inhalt)
    projekte.close()

def projekt_bearbeiten():
    projekte = database_connection()
    cursor = projekte.cursor()

    suche = input("Gib den Projektnamen ein: ")

    cursor.execute("SELECT * FROM projekte WHERE projektname LIKE ?", ('%' + suche + '%',))
    gefundene_projekte = cursor.fetchall()
    
    if not gefundene_projekte:
        print("Projekt nicht gefunden!")
        projekte.close()
        return
    
    projekt = gefundene_projekte[0]
    
    aendern = input(f"Ist dies {gefundene_projekte} das richtige Projekt? j/n: ").lower()

    if aendern == 'j':
        neuer_name = input("Neuer Projektname: ")
        
        cursor.execute("UPDATE projekte SET projektname = ? WHERE projektname = ?", (neuer_name, projekt[0]))
        projekte.commit()
        print("Projektname geändert!")
    else:
        print("Keine Änderung vorgenommen!")

    projekte.close()


def projekt_del():
    projekte = database_connection()
    cursor = projekte.cursor()

    suche = input("Gib den Projektnamen ein: ")

    cursor.execute("SELECT * FROM projekte WHERE projektname LIKE ?", ('%' + suche + '%',))
    gefundene_projekte = cursor.fetchall()
    
    if not gefundene_projekte:
        print("Projekt nicht gefunden!")
        projekte.close()
        return
    
    projekt = gefundene_projekte[0]

    delete = input(f"Möchtest du dieses {gefundene_projekte} löschen? j/n: ").lower()
    if delete == 'j':
        cursor.execute("DELETE FROM projekte WHERE projektname = ?", (projekt[0],))
        projekte.commit()
        print("Eintrag erfolgreich gelöscht!")
        projekte.close()
    else:
        print("Löschen abgebrochen!")
        projekte.close()


def neue_aufgabe():
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Welchem Projekt möchtest du eine Aufgabe hinzufügen? ")

    cursor.execute("SELECT * FROM projekte WHERE projektname LIKE ?", ('%' + aufgabe + '%',))
    gefundene_projekte = cursor.fetchall()


    if not gefundene_projekte:
        print("Kein Projekt gefunden!")
        return
    
    projekt = gefundene_projekte[0]
    korrekt = input(f"Möchtest du diesem Projekt {projekt} Aufgaben hinzufügen? j/n: ").lower()
    if korrekt == 'j':
        titel = input("Wie ist der Titel der Aufgabe? ")
        beschreibnung = input("Beschreibe die Aufgabe: ")
        datum = input("Fälligkeitsdatum: ")
        status = input("Status (offen, in bearbeitung, verschoben, erledigt): ")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aufgaben (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       projekt_id INTEGER,
                       titel TEXT,
                       beschreibung TEXT,
                       faelligkeitsdatum DATE,
                       status TEXT,
                       FOREIGN KEY (projekt_id) REFERENCES projekte(id)
            )
        ''')
        
        cursor.execute(
            "INSERT INTO aufgaben (projekt_id, titel, beschreibung, faelligkeitsdatum, status) VALUES (?, ?, ?, ?, ?)",
            (projekt[0], titel, beschreibnung, datum, status)
        )

        print("Aufgaben zum Projekt hinzugefügt!")

        projekte.commit()
        projekte.close()
    else:
        print("Abgebrochen!")
        projekte.close()


def aufgaben_anzeigen():
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Die Aufgaben welches Projektes möchtest du anzeigen? ")
    cursor.execute("SELECT * FROM projekte WHERE projektname LIKE ?", ('%' + aufgabe + '%',))
    gefundene_projekte = cursor.fetchall()


    if not gefundene_projekte:
        print("Kein Projekt gefunden!")
        return
    
    projekt = gefundene_projekte[0]
    projekt_id = projekt[0]

    cursor.execute("SELECT * FROM aufgaben WHERE projekt_id = ?", (projekt_id,))
    gefundene_aufgaben = cursor.fetchall()
    
    if not gefundene_aufgaben:
        print(f"Keine Aufgaben für das Projekt {aufgabe} gefunden!")
    else:
        print(f"Aufgaben für das Projekt {aufgabe}: ")
        for aufgabe in gefundene_aufgaben:
            print(f"Titel: {aufgabe[2]}, Beschreibung: {aufgabe[3]}, Fälligkeitsdatum: {aufgabe[4]}, Status: {aufgabe[5]}")
    projekte.close()

def aufgabe_bearbeiten():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du bearbeiten? ")
    aufgabe_neu = projekte_laden()
    gefundene_projekte = [projekt for projekt in aufgabe_neu if aufgabe == projekt['Projektname']]

    if not gefundene_projekte:
        print("Kein Projekt gefunden!")
        return
    
    projekt = gefundene_projekte[0]
    korrekt = input(f"Möchtest du die Aufgaben dieses Projekts {projekt} ändern? j/n: ").lower()
    if korrekt == 'j':
        aufgaben_alt = input("Welche Aufgabe möchtest du bearbeiten? ")
        gefundene_aufgabe = [aufgabe for aufgabe in projekt['Aufgaben'] if aufgaben_alt == aufgabe['Titel']]
        abfrage = input(f"Ist das {gefundene_aufgabe} die richtige Aufagbe? j/n: ")
        if abfrage == 'j':
            neuer_titel = input("Gib den neuen Titel der Aufgabe ein: ")
            neue_beschreibung = input("Gib eine neue Beschreibung ein: ")
            neues_datum = input("Gib ein neues Datum ein: ")
            neuer_status = input("Gib einen neuen Status ein (offen, in bearbeitung, verschoben, erledigt): ")
            index = projekt['Aufgaben'].index(gefundene_aufgabe[0])
            projekt['Aufgaben'][index] = {'Titel': neuer_titel, 'Beschreibung': neue_beschreibung, 'Datum': neues_datum, 'Status': neuer_status}
            projekt_speichern(aufgabe_neu)
            print("Bearbeitete Aufgabe zum Projekt hinzugefügt!")
        else:
            print("Aufgabe nicht gefunden!")

    else:
        print("Vorgang abgebrochen!")


def aufgabe_del():
    aufgabe = input("Die Aufgaben welches Projektes möchtest du löschen? ")
    aufgabe_neu = projekte_laden()
    gefundene_projekte = [projekt for projekt in aufgabe_neu if aufgabe == projekt['Projektname']]

    if not gefundene_projekte:
        print("Kein Projekt gefunden!")
        return
    
    projekt = gefundene_projekte[0]
    korrekt = input(f"Ist dies {projekt} das richtige Projekt? j/n: ").lower()
    if korrekt == 'j':
        alle = input("Möchtest du alle Aufgaben löschen? j/n: ").lower()
        if alle == 'j':
            projekt['Aufgaben'].clear()
            print("Alle Aufgaben gelöscht!")
        else:
            print(projekt['Aufgaben'])
            welche = input("Welche Aufgabe möchtest du löschen? Tippe hier: ")
            gefundene_aufgabe = [aufgabe for aufgabe in projekt['Aufgaben'] if welche == aufgabe['Titel']]
            projekt['Aufgaben'].remove(gefundene_aufgabe[0])
            projekt_speichern(aufgabe_neu)
            print("Aufgabe erfolgreich gelöscht!")

        if not welche:
            print("Keine Aufgabe gefunden!")
            return
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
    aufgabe = input("Die Aufgabe welches Projektes möchtest du als erledigt markieren? ")
    ergebnis = list(filter(lambda projekt: projekt['Projektname'] == aufgabe, projekte))

    if not ergebnis:
        print("Kein Ergebnis!")
        return
    
    projekt = ergebnis[0]
    korrekt = input(f"Ist dies {projekt} das richtige Projekt? j/n: ").lower()
    if korrekt == 'j':
        aufgabe_erledigt = input("Welche Aufgabe möchtest du als erledigt markieren? ")
        aufgaben_suche = list(filter(lambda aufgabe: aufgabe['Titel'] == aufgabe_erledigt, projekt['Aufgaben']))

        if not aufgaben_suche:
            print("Keine Aufgabe gefunden!")
            return
        
        aufgabe_ergebnis = aufgaben_suche[0]
        check = input(f"Möchtest du diese Aufgabe {aufgabe_ergebnis} als erledigt markieren? j/n: ").lower()
        if check == 'j':
            neuer_status = input("Gib einen neuen Status ein (offen, in bearbeitung, verschoben, erledigt): ")
            index = next(i for i, aufgabe in enumerate(projekt['Aufgaben']) if aufgabe['Titel'] == aufgabe_erledigt)
            projekt['Aufgaben'][index]['Status'] = neuer_status
            print("Aufgabe als erledigt markiert!")
        else:
            print("Aufgabe nicht gefunden!")


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