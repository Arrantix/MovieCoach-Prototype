# MovieCoach

Ein früher Python-Prototyp aus dem Unterricht: Zwei Personen markieren Filme, die sie sehen möchten. MovieCoach zeigt gemeinsame Treffer und kann bereits gesehene Vorschläge ausblenden.

Das ursprüngliche Kursprojekt entstand im Team. Die Python-Implementierung habe ich übernommen; Konzept, Gestaltung und Dokumentation wurden gemeinsam entwickelt. Verweise auf die weiteren Beteiligten werden ergänzt.

## Diese öffentliche Fassung

Die Demo wurde für eine sichere Veröffentlichung auf den Kern der Idee reduziert. Sie nutzt zwei lokale Beispielprofile (`A` und `B`), eine SQLite-Datenbank und sechs **frei erfundene** Filmtitel. Die ursprüngliche Datenbank mit Konten, Passwörtern, Bewertungen und einem externen Filmkatalog wurde nicht übernommen. Es gibt keine Anmeldung und keinen Online-Dienst.

```sh
python moviecoach.py init
python moviecoach.py movies
python moviecoach.py vote A 1 like
python moviecoach.py vote B 1 like
python moviecoach.py matches
python moviecoach.py watched 1
```

Die Demo-Datenbank `moviecoach.db` entsteht lokal durch `init` und ist von Git ausgeschlossen. `schema.sql` dokumentiert die Struktur und die künstlichen Beispieldaten.

Tests: `python -m unittest discover -s tests`. Benötigt nur die Python-Standardbibliothek (Python 3.10+).

**Stand:** Unterrichtsprototyp und kuratierte CLI-Demo. Dies ist keine fertige Filmplattform.
