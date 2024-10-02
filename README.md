# Projekt Management Tool

## Installation

Python 3 muss auf deinem Rechner installiert sein. Du kannst es hier herunterladen.
Speichere den Code in einer Datei, z.B. projektmanager.py.

## Ausführung

Um das Skript auszuführen, öffne ein Terminal und navigiere in das Verzeichnis, in dem die Datei gespeichert ist. Verwende dann folgenden Befehl:

bash
Code kopieren
python projektmanager.py
Das Menü wird angezeigt, und du kannst durch Eingabe der entsprechenden Zahl die gewünschte Funktion auswählen.

# Funktionen

## 1. neues_projekt()

Diese Funktion erstellt ein neues Projekt. Der Benutzer gibt den Projektnamen, das Startdatum und die Priorität ein. Das Projekt wird dann zur Liste projekte hinzugefügt.

Eingabe:
Projektname
Startdatum
Priorität
Ergebnis: Ein neues Projekt wird erstellt und der Liste hinzugefügt.

## 2. projekt_anzeigen()

Zeigt alle gespeicherten Projekte und deren Details in der Konsole an.

Eingabe: Keine
Ergebnis: Alle Projekte werden in der Konsole ausgegeben.

## 3. projekt_bearbeiten()

Ermöglicht das Bearbeiten eines bestehenden Projekts. Der Benutzer gibt den Projektnamen ein, und wenn das Projekt existiert, kann der Name geändert werden.

Eingabe:
Projektname
Neuer Projektname
Ergebnis: Der Name des Projekts wird geändert.

## 4. projekt_del()

Löscht ein Projekt basierend auf dem Projektnamen. Der Benutzer wird zur Bestätigung aufgefordert.

Eingabe:
Projektname
Bestätigung
Ergebnis: Das Projekt wird gelöscht, sofern es gefunden wurde.

## 5. neue_aufgabe()

Fügt einer bestehenden Projektaufgabe eine neue Aufgabe hinzu. Der Benutzer muss den Titel, die Beschreibung, das Fälligkeitsdatum und den Status der Aufgabe angeben.

Eingabe:
Projektname
Titel der Aufgabe
Beschreibung
Fälligkeitsdatum
Status (offen, in Bearbeitung, verschoben, erledigt)
Ergebnis: Eine neue Aufgabe wird zum Projekt hinzugefügt.

## 6. aufgaben_anzeigen()

Zeigt die Aufgaben eines ausgewählten Projekts an.

Eingabe: Projektname
Ergebnis: Die Aufgaben des Projekts werden in der Konsole angezeigt.

## 7. aufgabe_bearbeiten()

Ermöglicht das Bearbeiten einer Aufgabe innerhalb eines Projekts. Der Benutzer kann den Titel, die Beschreibung, das Fälligkeitsdatum und den Status ändern.

Eingabe:
Projektname
Aufgabentitel
Neuer Titel
Neue Beschreibung
Neues Fälligkeitsdatum
Neuer Status
Ergebnis: Die ausgewählte Aufgabe wird bearbeitet.

## 8. aufgabe_del()

Löscht eine oder alle Aufgaben aus einem Projekt.

Eingabe:
Projektname
Aufgabentitel (oder Option zum Löschen aller Aufgaben)
Ergebnis: Die Aufgabe oder alle Aufgaben des Projekts werden gelöscht.

## 9. aufgabe_sort()

Sortiert die Aufgaben eines Projekts entweder nach Datum oder nach Status.

Eingabe:
Projektname
Sortierkriterium (Datum oder Status)
Ergebnis: Die Aufgaben des Projekts werden in der Konsole sortiert angezeigt.

## 10. aufgabe_erledigt()

Markiert eine bestimmte Aufgabe als erledigt, indem der Status geändert wird.

Eingabe:
Projektname
Aufgabentitel
Neuer Status
Ergebnis: Die Aufgabe wird als erledigt markiert.

## 11. beenden()
Beendet das Programm.

## Menü
Das Skript verwendet eine Menüführung, um die oben beschriebenen Funktionen auszuführen. Du kannst eine Zahl eingeben, um die entsprechende Funktion zu nutzen:

1. Neues Projekt erstellen
2. Projekte anzeigen
3. Projekt bearbeiten
4. Projekt löschen
5. Neue Aufgabe zu einem Projekt hinzufügen
6. Aufgaben anzeigen
7. Aufgabe bearbeiten
8. Aufgabe löschen
9. Aufgaben sortieren
10. Aufgabe als erledigt markieren
11. Programm beenden

Wähle die gewünschte Option durch Eingabe der entsprechenden Zahl.