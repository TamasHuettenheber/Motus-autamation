# Jori & Flimm – Staffel 1, Folgen 001–005 – Produktionsübergabe V1

**Stand 22. Oktober 2026.**

## Umgesetzt
- Fünf neue eigenständige zusammenhängende Geschichten in `kids/jori-flimm/relaunch-v2/staffel1_folgen_001_005.json`.
- Fünf **tatsächlich gerenderte**, abspielbare Vorschau-MP4-Dateien, jeweils 720 × 1280, H.264, AAC, 6 Szenen, Jori/Flimm-Illustrationsstil.
- Verbindlicher Ablauf pro Folge: aufregender Einstieg, Handlung, sichtbare konkrete Rätselobjekte, gesprochene Frage, sieben Sekunden Stille, gesprochene Lösung, ein Cliffhanger für die nächste Episode.
- Alte Folge 000–003 nicht überschrieben. Neue Staffel beginnt ausdrücklich mit Folge 001.
- Sprecher-ID **Sulafat** für alle fünf Episoden. 001/004 mit Gemini 3.8 Flash TTS; 002/003/005 nach HTTP-429-Drosselung des Flash-Modells mit Gemini 3.8 Flash-Lite TTS (gleiche benannte Stimme, mögliches Klanggefälle).
- Rätselvisualisierungen zusätzlich zu bestehenden Jori-&-Flimm-Illustrationen gezeichnet; konkrete Bilder zeigen 001 Mond/Sonne/Stern, 002 Blau/Gold/Blau/?, 003 2/4/6/?, 004 Kreis-/Dreieck-/Quadrat-Schloss und dreieckige Schlüsselspitze, 005 vier Laternen, davon drei beleuchtet. Storys greifen die Hinweise hörbar auf und führen logisch zum nächsten Cliffhanger.
- Alle MP4-Dateien, dazu Drehbuch und technische Prüfung, liegen in der persönlichen Bibliothek unter `/Jori & Flimm/Staffel 1/Jori_Flimm_Staffel1_Folgen_001_bis_005_Arbeitsfassungen.zip` (40 MB). Das ist eine beständige ZIP-Kopie, kein GitHub-Release.
- Kein TikTok-Publishing, keine MOTUS-Workflows verändert, kein Merge in `main`.

## Technisch gemessen (jeweils tatsächlich finale MP4)
| Folge | Titel | Dauer | Integrierte Lautheit | True Peak | Denkpause |
|---|---|---:|---:|---:|---|
| 001 | Das Licht, das Joris Namen kannte | 86.4 s | -14.85 LUFS | -4.55 dBTP | 7 s nachgewiesen |
| 002 | Drei Klopfzeichen im Laternenlicht | 79.1 s | -14.70 LUFS | -4.71 dBTP | 7 s nachgewiesen |
| 003 | Die Tür, die niemand sehen konnte | 82.0 s | -14.57 LUFS | -4.76 dBTP | 7 s nachgewiesen |
| 004 | Das falsche Schloss | 77.8 s | -14.62 LUFS | -4.68 dBTP | 7 s nachgewiesen |
| 005 | Die Gestalt im Schneesturm | 79.3 s | -14.08 LUFS | -4.71 dBTP | 7 s nachgewiesen |

Die erreichte Lautheit belegt eine messbare Datei, nicht tatsächliche iPhone-Lautsprecherlautstärke. Die angegebene Pause wurde in den AAC-Streams via ffmpeg `silencedetect` überprüft.

## Freigabestand: NICHT RELEASE-READY
**Die fünf MP4 sind Arbeitsfassungen und nicht die vom Nutzer geforderte vollständige redaktionelle Endabnahme.**

Noch nicht bestanden:
1. **Wortgenaue, zeitlich geprüfte Untertitel.** Um die vom Nutzer kritisierte falsche Wort-/Tonsynchronisierung nicht zu wiederholen, zeigen diese Fassungen kurze gezielte Handlungstafeln, Rätsel und Lösungen, aber keine fälschlich wortgenau synchronisierten Volltext-Untertitel. Eine echte ASR-Zeitachsen-Ermittlung und Endkontrolle sind erforderlich.
2. **Motivgenaue neue Szenenbilder.** Bestehende kanonische Charakterbilder wurden mit individuell gezeichneten Rätsel-/Objektkarten neu komponiert. Die für alle sechs Szenen nötigen eigens illustrierten, handlungstreuen Hintergründe fehlen noch.
3. **Vollständiger redaktioneller Seh- und Hörtest**, einschließlich echter iPhone-Abspielbarkeit, exakter TTS-Worttreue, Falschpronunziationen, Ton/Schrift und Bild zu jedem Satz, fehlt.
4. **Tägliche GitHub-Liveproduktion und Veröffentlichung 14:00** ist nicht aktiviert. Reproduzierbarer Video-Renderer wurde für diese Arbeitsfassungen lokal ausgeführt; neuer Ablauf ist **noch nicht automatisiert nach GitHub integriert**.
5. Verfügbarkeit des kostenlosen TTS-Kontingents und Klangkonstanz bei Modellvarianten nach HTTP-429 müssen vor einem unbeaufsichtigten Dauerbetrieb nachgewiesen werden.

## GitHub-Automation und Testnachweise
- PR/Altzweig: `feature/jori-flimm-kids-pipeline` bleibt unverändert / MOTUS `main` ist isoliert.
- Neuer Staffelzweig: `feature/jori-flimm-neustart-folge001`.
- Einmaliger gemeinsamer Voice-Test: Run 39689357052 (2/5 erfolgreich, restliche HTTP 429).
- Serieller Wiederholungsversuch: Run 39689569865 (alle drei HTTP 429, kein kostenpflichtiger Fallback).
- Sulafat Flash-Lite: Run 39690134835 (Folge 002 erfolgreich), Run 39690251735 (Folgen 003 und 005 erfolgreich).
- Story-QC-Regressionstests: Run 39688428426 (12/12 bestanden). Diese Tests prüfen Code-/Schema-Logik, **nicht** den Abschluss sämtlicher inhaltlicher Videoprüfungen.

## Nächste Arbeit ohne neue Nutzerangaben
1. Story-/Bild-Satz-Matching für fünf Folgen und individuelles Illustrationspaket.
2. Reale ASR-/forced-alignment Untertitel erstellen und audio-to-text Worttreue prüfen; alte proportional verteilte Untertitel ersetzen.
3. Die fünf vollständigen MP4 neu rendern; jedes von Anfang bis Ende prüfen.
4. iPhone-Wiedergabe bestätigen und schließlich fünf fertige Publikationspakete mit Tatsachenstatus ausgeben.
5. GitHub-Videopipeline erst nach vollständiger Testkette zum regelmäßigen unüberwachten Betrieb freigeben.

Keine kostenpflichtigen Verpflichtungen eingegangen.
