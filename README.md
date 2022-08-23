
# How to start the Dielectric Measurement Database App?

`python ./src/DielectricMeasurementsAPP.py`


# Dependencies: What to install first
* Python 3.10 is needed to run this!, so install: https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5
* `pip install matplotlib`
* `pip install pandas`
* `pip install pandastable`
* `pip install PIL`
* `pip install tkinter`

## Anforderungen

Ziel des Projektes:

Als Laborant möchte ich Permittivitätsmessergebnisse miteinander vergleichen, um den optimalen Werkstoff auszuwählen.

### Veröffentlichen
Als Laborant möchte ich Permittivitätsmessergebnisse(CSV) in einer Datenbank speichern, um diese zu zu veröffentlichen.

Tasks:
* CSV einlesen
* Permittivitäts-Datenbank und Datenbankschema erstellen
* CSV in Permittivitäts-Datenbank ablegen

### Auswerten
Als Laborant möchte ich Permittivitätsmessergebnisse miteinander vergleichen, um den optimalen Werkstoff auszuwählen.

#### Frequenz Vergleich: Eigenschaften der Werkstoffe auf einer Frequenz vergleichen
* Diagramm 1: Als Laborant möchte ich die Frequenzverläufe aller Werkstoffe sehen, um ihre Permitivität zu vergleichen.
* Tabelle 1: Als Laborant möchte ich die Messergebnisse aller Werkstoffe bei einer gemessenen Frequenz anzeigen, um diese zu vergleichen.
* Spalten-Filter: Als Laborant möchte ich bestimmte Spalten ausblenden, damit ich eine bessere Übersicht habe.
* Frequenz-Filter: Als Laborant möchte ich gemessene Frequenzen auswählen, um Werkstoffe auf einer bestimmten Frequenz zu vergleichen.

### Werkstoffdetails: Eigenschaften eines Werkstoffes auf gemessenen Frequenzen vergleichen
* Tabelle 2: Als Laborant möchte ich die Ergebnisse eines Werkstoffes in einer Tabelle anzeigen, um diese zu vergleichen.
* Spalten-Filter: Als Laborant möchte ich bestimmte Spalten ausblenden, damit ich eine bessere Übersicht habe.
* Werkstoff-Auwahl: Als Laborant möchte bereits gemessene Werkstoffe auswählen, um mir dessen Ergebnisse anzuzeigen.
* Diagramm 2: Als Laborant möchte ich den Frequenzverlauf einer Messung sehen, um deren Verlauf zu analysieren.

## Implementierung

Datenbankschema
* Measurements/Mesungen (ID, Name,	Temperature [°C],	Humidity [%],	Material type,	Serial number, PDC output voltage (DC) [V],	FDS output voltage (AC) [V],	c0	Sample thickness [m])
* FDS RESULT/Messreihen (IDMessung(FK),	Frequency [Hz],	Tanδ	εr',	εr'',	|Z| [Ω],	Phase of Z [°],	|Y| [S],	Phase of Y [°],	Cp [F],	Rp [Ω],	c' [F],	c'' [F],	R [Ω],	X [Ω])