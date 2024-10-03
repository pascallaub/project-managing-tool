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
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Die Aufgaben welches Projektes möchtest du bearbeiten? ")
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
        projekte.close()
        return
    
    print(f"Aufgaben für das Projekt {aufgabe}: ")
    for idx, aufgabe in enumerate(gefundene_aufgaben):
        print(f"{idx + 1}. Titel: {aufgabe[2]}, Beschreibung: {aufgabe[3]}, Fälligkeitsdatum: {aufgabe[4]}, Status: {aufgabe[5]}")

    aufgaben_index = int(input("Welche Aufgabe möchtest du bearbeiten? (Nummer eingeben): ")) - 1

    if 0 <= aufgaben_index < len(gefundene_aufgaben):
        auszuwaehlende_aufgabe = gefundene_aufgaben[aufgaben_index]

        neuer_titel = input(f"Neuer Titel (aktuell: {auszuwaehlende_aufgabe[2]}): ") or auszuwaehlende_aufgabe[2]
        neue_beschreibung = input(f"Neue Beschreibung (aktuell: {auszuwaehlende_aufgabe[3]}): ") or auszuwaehlende_aufgabe[3]
        neues_datum = input(f"Neues Fälligkeitsdatum (aktuell: {auszuwaehlende_aufgabe[4]}): ") or auszuwaehlende_aufgabe[4]
        neuer_status = input(f"Neuer Status (aktuell: {auszuwaehlende_aufgabe[5]}): ") or auszuwaehlende_aufgabe[5]

        cursor.execute('''
            UPDATE aufgaben
            SET titel = ?, beschreibung = ?, faelligkeitsdatum = ?, status = ?
            WHERE id = ?''', 
            (neuer_titel, neue_beschreibung, neues_datum, neuer_status, auszuwaehlende_aufgabe[0]))
        
        projekte.commit()
        print("Aufgabe erfolgreich bearbeitet!")
    else:
        print("Ungültige Auswahl. Vorgang abgebrochen!")

    projekte.close()


def aufgabe_del():
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Die Aufgaben welches Projektes möchtest du löschen? ")
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
        projekte.close()
        return
    
    print(f"Aufgaben für das Projekt {aufgabe}: ")
    for idx, aufgabe in enumerate(gefundene_aufgaben):
        print(f"{idx + 1}. Titel: {aufgabe[2]}, Beschreibung: {aufgabe[3]}, Fälligkeitsdatum: {aufgabe[4]}, Status: {aufgabe[5]}")

    aufgaben_index = int(input("Welche Aufgabe möchtest du löschen? (Nummer eingeben): ")) - 1

    if 0 <= aufgaben_index < len(gefundene_aufgaben):
        auszuwaehlende_aufgabe = gefundene_aufgaben[aufgaben_index]

        cursor.execute("DELETE FROM aufgaben WHERE projekt_id = ?", (projekt[0],))
        print("Ausgabe erfolgreich gelöscht!")
        projekte.commit()
        projekte.close()
    else:
        print("Keine Auswahl getroffen!")
        projekte.close()

def aufgabe_sort():
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Die Aufgaben welches Projektes möchtest du sortiert anzeigen? ")
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
        projekte.close()
        return
    
    cursor.execute("SELECT * FROM `aufgaben` ORDER BY `titel`")
    for datensatz in cursor:
        print(datensatz)
        
    projekte.close()



def aufgabe_erledigt():
    projekte = database_connection()
    cursor = projekte.cursor()

    aufgabe = input("Die Aufgaben welches Projektes möchtest du als erledigt markieren? ")
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
        projekte.close()
        return
    
    print(f"Aufgaben für das Projekt {aufgabe}: ")
    for idx, aufgabe in enumerate(gefundene_aufgaben):
        print(f"{idx + 1}. Titel: {aufgabe[2]}, Beschreibung: {aufgabe[3]}, Fälligkeitsdatum: {aufgabe[4]}, Status: {aufgabe[5]}")

    aufgaben_index = int(input("Welche Aufgabe möchtest du als erledigt markieren? (Nummer eingeben): ")) - 1

    if 0 <= aufgaben_index < len(gefundene_aufgaben):
        auszuwaehlende_aufgabe = gefundene_aufgaben[aufgaben_index]

        neuer_status = input(f"Neuer Status (aktuell: {auszuwaehlende_aufgabe[5]}): ") or auszuwaehlende_aufgabe[5]

        cursor.execute('''
            UPDATE aufgaben
            SET status = ?
            WHERE id = ?''', 
            (neuer_status, auszuwaehlende_aufgabe[0]))
        
        projekte.commit()
        print("Aufgabe erfolgreich als erledigt markiert!")
    else:
        print("Ungültige Auswahl. Vorgang abgebrochen!")

    projekte.close()


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