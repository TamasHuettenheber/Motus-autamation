# Folge 001 V8 – Korrektur des abrupten Anfangs und Staffel-Vielfalt

Stand 22.10.2026. Nutzer fand Rätsel und Darstellung in V7 gelungen, aber die Einleitung "Jori und Flimm. Folge eins" mit unmittelbar anschließender mitten-in-der-Handlung-Szene nicht nachvollziehbar. Zudem Sorge, dass alle fünf Folgen dieselbe Geschichte erzählen.

## V8 tatsächlich erstellt (private Prüffassung)
- **Neuer eigenständiger Prolog** mit Sulafat: „Mitten in einer Winternacht hörte Jori plötzlich seinen Namen. Aber niemand war zu sehen. Noch wusste er nicht, dass er gleich Flimm kennenlernen würde. Hier beginnt ihre Geschichte: Jori und Flimm. Folge eins.“
- Neu generierte 17,32 Sekunden Sprecheraufnahme, unveränderte freigegebene Stimme Sulafat, GitHub-Actions-Erfolg: https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39741634495.
- Prolog zeigt Jori **vor** dem Kennenlernen allein auf dem verschneiten Weg und ein geheimnisvolles Leuchten. Die vorherige kurze V7-Ansage (3,75 s) wurde entfernt; danach beginnt die eigentliche Handlung mit „Plötzlich flackerte ein Licht unter dem Schnee ...“.
- Vorhandenes, vom Nutzer gelobtes Rätsel **Mond/Sonne/Stern** samt eingeblendeter Frage und Denkpause bleibt in der übrigen Geschichte unverändert.
- Lokale V8: `/mnt/data/jori_rework_001/Jori_Flimm_Folge_001_Neu_V8_Mit_Echtem_Anfang_Prueffassung.mp4` (8,23 MB, 103,17 s, 720×1280, H.264/AAC). Gemessene integrierte Lautheit −13,8 LUFS; true peak −1,23 dBTP. `silencedetect` erkennt Rätsel-Stille ca. 72,22–79,69 s (7,47 s inklusive stiller Sprachübergänge).
- 11 Standbilder von Beginn bis Ende für Bildkontrolle geprüft. Intro zeigt Jori alleine, später Flimm; Rätselzeichen bleiben sichtbar. Bilder sind aus vorhandenem, konsistentem Figurenbestand, nicht komplett neu gezeichnet.
- **Keine TikTok-Veröffentlichung, keine Buffer-Buchung**, da Wort-für-Wort-Synchronisierung, vollständige Abnahme und stabiles Video-Hosting weiterhin offen.

## Staffelweite dramaturgische Absicherung
- `relaunch-v2/SERIENBIBEL_GESCHICHTEN_VIELFALT.md` definiert unterschiedliche Charakterentwicklung, Schauplätze, Rätseltypen und Cliffhanger für 001–005 sowie Anschluss 006.
- `relaunch-v2/scripts/generate_episode.py` enthält zusätzlich konkrete Anti-Wiederholungsregeln für Folge 006+; Flimm wird nicht in jeder Episode neu entdeckt.
- Keine alten Dateien überschrieben; V7 bleibt zum Vergleich vorhanden.

## Noch zu erledigen
1. Sprechertext und Untertitel der gesamten V8 **wort- und zeitgenau** abgleichen (im Prolog bisher ungefähr nach Satzlänge verteilt, keine ASR-Verifizierung).
2. Endabnahme von Bild zu Handlung und tatsächliche Wiedergabe auf Nutzerhandy.
3. Nach finaler Freigabe Videodatei stabil öffentlich hosten und in Buffer für den tatsächlich noch möglichen Veröffentlichungstermin einstellen. Niemals einen Erfolg behaupten, bevor Buffer eine Post-ID liefert.
4. Neue Episoden 002–005 nach denselben verbindlichen Regeln prüfen und ggf. angleichen.
