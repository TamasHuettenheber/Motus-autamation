# MOTUS-Qualitätsstand – Vorgang MOTUS-Q01

Stand: 2026-11-15 · Besitzer: Motus Analyse & Optimierung  
**Status: KORRIGIERT / PRODUKTIONSWIRKUNG_OFFEN**

## Ursachennachweis
Die bisherige A/B-Qualitätsprüfung ließ bei kurzen Skripten 30–55 Wörter und bei langen 55–85 zu, obwohl der Test 35–45 / 65–75 verlangte. Die vier festen Schluss-CTAs und generischen Ergänzungssätze machten zurückgewiesene KI-Texte eintönig. Im 14-Tage-Themenraster fehlte eine semantische Vier-Slot-Kollisionsprüfung. Der B-Roll-Selektor wertete Teilzeichenketten fälschlich als Szene: In Issue #108 wurde wegen `zug` innerhalb von `dazugelernt` ein Zug/Telefon-Clip für das 07:00-Video ausgewählt; `ziel` innerhalb von `gezielt` führte zu einer falschen Planungsszene.

Die reguläre Produktion von [MOTUS-DAY] 2026-11-16 (#108) auf Workflow-Lauf 43656868221 zeigte vor dieser Reparatur: 40/73/35/67 Wörter, drei `EDITORIAL_QC_PASS` und eine `EDITORIAL_QC_REPLACED` (22:00, 92 → 67 Wörter); alle vier `LENGTH_AB_QC`. Diese Ausgabe ist **kein** Nachweis der neuen Änderung.

## Tatsächliche Änderung auf main
- `config/motus-editorial-cards.json`: 56 Karten mit semantischem Motiv versehen; 30 motivbezogene, handgeschriebene Ergänzungssätze-Gruppen für den Ersatztext hinterlegt. Commits `3aa1fd9d`, `0c248f11`, `aa847fc0`.
- `.github/workflows/motus-night-production.yml`: Motiv-Offsets für 18:30 und 22:00 mit vier unterschiedlichen Tagesmotiven; 16 CTA-Formulierungen in vier rotierenden Arten; motivbezogener Fallback statt Standard-Phrasen; Zielwortgrenzen 35–45 / 65–75 verbindlich; zusätzliche Prüfung auf gleichlautende Tagesideen. Commit `7f2dc554`.
- `.github/workflows/motus.yml`: generische Gefühlswörter ohne Bildbezug aus Ranking entfernt; echte Wortgrenzen statt Teilzeichenketten; vier slotgerechte Szenenpools; bei gleicher Trefferqualität passende Szene bevorzugt. Commits `a69f12a5`, `9f25aa19`, `fc4e14e9`.

## Tests / Rückprüfung
Die GitHub-Readbacks der drei Quelldateien nach den Commits waren erfolgreich. Die aus den **aktuellen** 56 Karten und Motiv-Ergänzungen abgeleitete Fallback-Auswahl wurde für 28 aufeinanderfolgende Tage mit 112 Slotfällen kontrolliert durchgerechnet: **112/112** korrekte A/B-Wortzahlen, **0** gleichartige Tagesmotive, **0** CTA-Typ-Kollisionen. Der B-Roll-Abgleich gegen die vier echten Skripte aus #108 und die vorhandenen 30 Clip-Metadaten zeigt jetzt, dass `zug` in `dazugelernt` sowie `ziel` in `gezielt` nicht mehr treffen. Dies sind nachvollziehbare Konfigurations-/Logik-Dry-Runs, **noch keine neuen Videorender oder GitHub-Runner-Tests**.

Diff/gezielter Rückweg: Vergleich der drei geänderten Dateien vom Ausgangscommit `cf6e44b5ce5ed0aee3b70615303bd2b096e57cdc` zum letzten Änderungscommit `fc4e14e9b9496a4d480012ea6f1b4e95a4dee534` (7 Commits). Bei Rückbau ausschließlich die betroffenen Dateien mit jeweils aktuellem SHA wiederherstellen, keinen unkontrollierten Branch-Reset.

## Nächste Voraussetzung
Auf den nächsten **regulär** mit neuer Logik erzeugten Tagesauftrag warten und dessen tatsächliche `EDITORIAL_QC_PASS/REPLACED`, vier `LENGTH_AB_QC`, Themen sowie nachgelagerte `BROLL_RELEVANCE_QC`-Auswahl prüfen; dann erst die Produktionswirkung bewerten. Kein Workflowstart, Issue, Duplikat, Bezahlvorgang oder Eingriff in bestehende/terminierte/veröffentlichte Videos. Vier Slots und Google-Gemini/Algenib unverändert.

Performance-Status: Die in diesem Lauf erreichbaren Metricool-Datensätze reichten nur bis 12.11.2026; die hier abgefragten TikTok-Watchtime-/Retention-Felder waren leer. Es gibt keine belegte Reichweitenverbesserung.

Ablage: Library-Ziel `/Hüttenheber Digital/01_Agenten/MOTUS_Qualitaet` wurde versucht; `files.manage_library` meldete für Ordner und Upload `AccessDeny`. Deshalb liegt dieser Arbeitsstand als unmittelbar erreichbares, kontrollierbares GitHub-Lieferobjekt vor. Workstation-Verbindung laut Nutzer vorhanden; die Desktop-Commander-Liste dieses Laufs zeigte ausschließlich die nicht verwendete Rezeption. GitHub-Schreibweg war funktionsfähig.

Technische Produktions-/Buffer-/Veröffentlichungs-Recovery bleibt bei `MOTUS – Technik & Reparatur`. Redaktionelle Korrekturen und deren Abnahme gehören MOTUS-Q01.
