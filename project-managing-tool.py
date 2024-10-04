from datetime import datetime
import sqlite3
import hashlib
import getpass

def database_connection():
    return sqlite3.connect("ProjekteDB/projects.db")

def user_database():
    return sqlite3.connect("UserDB/user.db")

def user_permissions():
    return sqlite3.connect("UserDB/rbac.db")
    
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

def register():
    login_connection = user_database()
    cursor = login_connection.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS userdata (
                benutzername TEXT NOT NULL,
                passwort BLOB NOT NULL
                )
            ''')
    cursor.execute("ALTER TABLE userdata ADD COLUMN role_id INTEGER")

    roles()

    username = input("Wähle einen Benutzernamen: ")

    cursor.execute("SELECT * FROM userdata WHERE benutzername = ?", (username,))
    result = cursor.fetchone()

    if result:
        print("Benutzername bereits vergeben! Wähle einen anderen!")
        login_connection.close()
        register()
        return
    
    passwort = getpass.getpass("Wähle ein Passwort: ")
    passwort_check = getpass.getpass("Wiederhole dein Passwort: ")

    if passwort_check == passwort:
            passwort_hash = hashlib.pbkdf2_hmac(
                'sha256',
                passwort.encode('utf-8'),
                b'some_salt',
                100000
            )
            cursor.execute("INSERT INTO userdata (benutzername, passwort) VALUES(?,?)", (username, passwort_hash))
            login_connection.commit()
            assign_role(username, 'user')
    else:
        print("Falsche Eingabe. Starte Vorgang erneut!")
        register()

    login_connection.close()
    login_menu()

def assign_role(username, role):
    permission_conn = user_permissions()
    cursor = permission_conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_roles (
                   benutzername TEXT NOT NULL,
                   role_name TEXT NOT NULL,
                   FOREIGN KEY (role_name) REFERENCES roles(role_name)
                   )
                ''')
    
    cursor.execute("INSERT INTO user_roles (benutzername, role_name) VALUES (?, ?)", (username, role))
    permission_conn.commit()
    permission_conn.close()

def login_menu():
    login_connection = user_database()
    cursor = login_connection.cursor()

    username = input("Benutzername: ")
    password = getpass.getpass("Passwort: ")

    cursor.execute("SELECT passwort FROM userdata WHERE benutzername = ?", (username,))
    result = cursor.fetchone()

    if result:
        stored_passwaord_hash = result[0]

        passwort_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'some_salt',
            100000
        )

        if passwort_hash == stored_passwaord_hash:
            print("Login erfolgreich!")
            menu()
        
        else:
            print("Ungültiges Passwort!")
    else:
        print("Benutzername nicht gefunden!")
    
    login_connection.closer()

def del_user():
    login_connection = user_database()
    cursor = login_connection.cursor()

    username = input("Benutzername: ")
    password = getpass.getpass("Passwort: ")

    cursor.execute("SELECT passwort FROM userdata WHERE benutzername = ?", (username,))
    result = cursor.fetchone()

    if result:
        stored_passwaord_hash = result[0]

        passwort_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'some_salt',
            100000
        )

        if passwort_hash == stored_passwaord_hash and username == 'Admin':
            print("Login erfolgreich!")

    cursor.execute("SELECT benutzername FROM userdata")
    users = cursor.fetchall()

    if users:
        print("Liste der Benutzer: ")
        for user in users:
            print(f"- {user[0]}")
        delete_explicit()
    login_connection.close()


def delete_explicit():
    login_connection = user_database()
    cursor = login_connection.cursor()
    
    username = input("Gib den Benutzernamen zum Löschen ein: ")

    cursor.execute("SELECT * FROM userdata WHERE benutzername = ?", (username,))
    result = cursor.fetchall()

    if result:
        confirm = input(f"Möchtest du den Benutzer {username} wirklich löschen? j/n: ").lower()
        if confirm == 'j':
            cursor.execute("DELETE FROM userdata WHERE benutzername = ?", (username,))
            login_connection.commit()
            print(f"{username} erfolgreich gelöscht!")
            again = input("Möchtest du einen weiteren Benutzer löschen? j/n: ").lower()
            if again == 'j':
                delete_explicit()
                return
            elif again == 'n':
                start_menu()
                return
            else:
                print("Löschvorgang abgebrochen!")
        else:
            print(f"{username} wurde nicht gefunden!")
    else:
        print("Es gibt keine Benutzer in der Datenbank!")
    
    login_connection.close()
    start_menu()

def change_role():
    login_connection = user_database()
    permission_conn = user_permissions()
    cursor_login = login_connection.cursor()
    cursor_permissions = permission_conn.cursor()

    username = input("Benutzername: ")
    password = getpass.getpass("Passwort: ")

    cursor_login.execute("SELECT passwort FROM userdata WHERE benutzername = ?", (username,))
    result = cursor_login.fetchone()

    if result:
        stored_password_hash = result[0]

        passwort_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'some_salt',
            100000
        )

        if passwort_hash == stored_password_hash:
            cursor_permissions.execute("SELECT role_name FROM user_roles WHERE benutzername = ?", (username,))
            user_role = cursor_permissions.fetchone()

            if user_role and user_role[0] == 'admin':
                user_to_change = input("Gib den Benutzernamen ein, dessen Rolle geändert werden soll: ")
                new_role = input("Neue Rolle (admin, manager, user): ")

                cursor_permissions.execute("UPDATE user_roles SET role_name = ? WHERE benutzername = ?", (new_role, user_to_change))
                permission_conn.commit()
                print(f"Rolle von {user_to_change} erfolgreich zu {new_role} geändert!")
            else:
                print("Du hast keine Berechtigung hierzu!")
        else:
            print("Falsches Passwort.")
    else:
        print("Benutzer nicht gefunden!")

    login_connection.close()
    permission_conn.close()



def start_menu():
    login = input("Einloggen (1), Registrieren (2) oder Benutzerrollen ändern (3) Benutzer löschen (4): ")
    if login == '1':
        login_menu()
    elif login == '2':
        register()
    elif login == '3':
        change_role()
    elif login == '4':
        del_user()
    else:
        print("Falsche Eingabe!")
        start_menu()


def roles():
    conn = user_permissions()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
                   id INTEGER PRIMARY KEY,
                   role_name TEXT UNIQUE
                   )
                ''')
    
    cursor.execute("INSERT INTO roles (role_name) VALUES ('admin'), ('manager'), ('user')")

    cursor.execute('''CREATE TABLE IF NOT EXISTS permissions(
                   id INTEGER PRIMARY KEY,
                   permission_name TEXT UNIQUE
                   )
                ''')
    
    cursor.execute("INSERT INTO permissions (permission_name) VALUES ('create'), ('read'), ('update'), ('delete')")

    cursor.execute('''CREATE TABLE IF NOT EXISTS role_permissions (
                   role_id INTEGER,
                   permission_id INTEGER,
                   FOREIGN KEY(role_id) REFERENCES roles(id),
                   FOREIGN KEY(permission_id) REFERENCES permissions(id))''')

    cursor.execute('''INSERT INTO role_permissions (role_id, permission_id)
                   VALUES ((SELECT id FROM roles WHERE role_name = 'admin'), (SELECT id FROM permissions WHERE permission_name = 'create')),
                          ((SELECT id FROM roles WHERE role_name = 'admin'), (SELECT id FROM permissions WHERE permission_name = 'read')),
                           ((SELECT id FROM roles WHERE role_name = 'admin'), (SElECT id FROM permissions WHERE permission_name = 'update')),
                            ((SELECT id FROM roles WHERE role_name = 'admin'), (SELECT id FROM permissions WHERE permission_name = 'delete'))
                    ''')
    
    cursor.execute('''INSERT INTO role_permissions (role_id, permission_id)
                   VALUES ((SELECT id FROM roles WHERE role_name = 'manager'), (SELECT id FROM permissions WHERE permission_name = 'create')),
                          ((SELECT id FROM roles WHERE role_name = 'manager'), (SELECT id FROM permissions WHERE permission_name = 'read')),
                           ((SELECT id FROM roles WHERE role_name = 'manager'), (SElECT id FROM permissions WHERE permission_name = 'update'))
                    ''')
    
    cursor.execute('''INSERT INTO role_permissions (role_id, permission_id)
                        VALUES  ((SELECT id FROM roles WHERE role_name = 'user'), (SELECT id FROM permissions WHERE permission_name = 'read'))
                    ''')
    
    conn.commit()
    conn.close()


def check_permission(username, action):
    conn = user_permissions()
    cursor = user_permissions.cursor()

    cursor.execute('''
            SELECT r.role_name
            FROM userdata u
            JOIN roles r ON u.role_ID = r.id
            WHERE u.username = ?
            ''', (username,))
    
    role = cursor.fetchone()

    if role is None:
        conn.close()
        return False
    
    cursor.execute('''
            SELECT p.permission_name
            FROM role_permissions rp
            JOIN roles r ON rp.role_id = r.id
            JOIN permissions p ON rp.permission_id = p.id
            WHERE r.role_name = ? AND p.permission_name = ?
            ''', (role[0], action))
    
    permission = cursor.fetchone()
    conn.close()

    return permission is not None




if __name__=='__main__':
    start_menu()