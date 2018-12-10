# Hunger

Kleines Python-Skript zum Abruf der Menüs der Gießener Hochschul-Mensen (JLU & THM).

## Anleitung

```
usage: hunger.py [-h]
                 [--mensa [{THM,MILF,Campustor,IFZ,CaRe,OBS} [{THM,MILF,Campustor,IFZ,CaRe,OBS} ...]]]
                 [--woche]

Wir haben Hunger, Hunger, Hunger ...

optional arguments:
  -h, --help            show this help message and exit
  --mensa [{THM,MILF,Campustor,IFZ,CaRe,OBS} [{THM,MILF,Campustor,IFZ,CaRe,OBS} ...]], -m [{THM,MILF,Campustor,IFZ,CaRe,OBS} [{THM,MILF,Campustor,IFZ,CaRe,OBS} ...]]
                        Welche Mensa?
  --woche, -w           Bunte Wochenübersicht ...
```

Durch Anlegen einer Datei ".hunger" im Benutzerverzeichnis kann man eine Standardliste von Mensen definieren. Hier eine Beispieldatei:

```
THM
Campustor
```

Diese wird dann automatisch beim nächsten Aufrufen des Skripts benutzt. Standardmäßig wird die THM Mensa abgerufen.