# Neustart und Qualitätsinventur Jori & Flimm – 22.10.2026

## Nutzerauftrag – verbindlich
Alle Videos vor einer Veröffentlichung erneut durch eine umfassende Qualitätskontrolle führen. **Neustart ab Folge 001**, mit Dramaturgie `spannender Einstieg → Geschichte → ein Rätsel → sieben Sekunden echte Denkpause → Lösung → spannender Cliffhanger`.

## Altmaterial – kein Video für neue Staffel freigegeben
| Historisches Material | Nachgewiesener Stand | Entscheidung |
|---|---|---|
| Alte Episode 000 | Frühes Intro, 3 Sekunden Rätselfrage-Pause im Episodenledger; technische Testvorschau | Nicht als neue Folge 001 übernehmen. Veraltete Pause und neue Dramaturgieregel |
| Alte Episode 001 | Technischer Renderer-Test vorhanden, Victoria-Stimme und nur geschätzte Untertitelzeit; keine vollständige inhaltliche, visuelle und Tonfreigabe | Für Neuauflage gesperrt |
| Alte Episode 002, erste Version | Handlung weitgehend über Igel statt Jori/Flimm; zu leise Stimme; wichtige Glockenbilder fehlen | Verworfen |
| Alte Episode 002, Piper-Revision | Lauter, aber aus Nutzersicht lehrerhafte, unpassende Sprecherin und unpassende Glockenbilder | Verworfen |
| Alte Episode 002, Sulafat-Revision | Nutzer bestätigt Sprecherin Sulafat als optimal; **Untertitel stimmen nicht immer mit Sprache überein, Aufzählungen brechen unnatürlich ab, Glockensymbole fehlen sichtbar** | Nicht freigegeben. Sprecherin wird beibehalten, alter Film verworfen |
| Alte Episode 003 | Historisch nur ein Storyentwurf; kein veröffentlichungsreifes Video | Kein Bestandteil des Neustarts |

**Keine der alten Versionen wurde zur neuen Staffel zugelassen.** Sie bleiben in der GitHub-Historie/alten Entwicklung, ohne Dateien zu überschreiben.

## Neue Staffel – realer Umsetzungsstand
- Neues isoliertes Branch: `feature/jori-flimm-neustart-folge001`.
- Neue kanonische Struktur in `relaunch-v2/REGELWERK.md`.
- Neustart-Serienstand `relaunch-v2/state/series-state.json`: letzte akzeptierte neue Episode `0`, nächste `1`, keine TikTok-Veröffentlichungsfreigabe.
- Aktuelle Sprecherin fest im Storygenerator und Preview-Compiler als `Gemini TTS 3.8 / Sulafat` hinterlegt.
- `relaunch-v2/scripts/generate_episode.py`: isolierte episodische KI-Textgenerierung und Formalprüfungen, bewusst ohne Publikationsmöglichkeit.
- `relaunch-v2/scripts/quality_gate.py`: ein **gesperrtes** Release-Gate. Verlangt 14 tatsächliche Prüfnachweise, echte Transkript- und Untertitelsynchronität, visuell nachgewiesene Hinweise, iPhone/Android-Abspieltest und dokumentierte Ganzfilm-Abnahme; bloße Render-Erfolgsmeldung reicht nicht.
- **12 Offline-Regressionstests bestanden**: [GitHub Actions Run 39688428426](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39688428426).
- Neue **Folge 001**, `Das Licht, das Joris Namen kannte`, liegt als strukturierter Text mit konkreten Bildanweisungen unter `relaunch-v2/drafts/jori-flimm-restart-2026-10-23-e001.json`. Story/Formal-QC bestanden; Audio, Untertitel, Abspielbarkeit, Illustrationen und redaktionelle Video-Freigabe stehen ausdrücklich auf `false`. Datum ist lediglich eine interne Planungskennung, **kein Veröffentlichungstermin**.

## Offen und gesperrt
1. Aus sechs konkreten Szene-Anweisungen **sechs neue, wirklich passende Bildmotive** mit konsistenten Figuren erzeugen, einschließlich lesbaren drei Wegweisern und Symbolen Mond, Sonne, Stern. Keine alten Bilder als Beweis verwenden.
2. Mit Sulafat neu vertonen; Satzaufzählungen natürlicher gestalten und tatsächliche Sprechtexte vor Montage prüfen.
3. Echte Wort-/Satz-Timestamp-Ausrichtung für Untertitel und Hörtext. Alte Heuristik „Zeiten proportional zur Wortzahl“ **nicht mehr als veröffentlichungsreif akzeptieren**.
4. Am fertigen MP4 sichtbare Rätselhinweise, exakt sieben Sekunden echte Stille und durchgehend sichtbare Frage verifizieren.
5. Lautheit im fertigen Film messen und zusätzlich **auf einem iPhone/Android wirklich anhören**; nicht bloß LUFS als Garantie betrachten.
6. Erst nach sieben vollständigen und bestandenen Produktionszyklen die neue Zeitsteuerung vorbereiten. Bis dahin keine TikTok-Verbindung, kein automatisches Publizieren, kein MOTUS-Eingriff.

## Realer KI-Test zur neuen Staffel
- Drei begrenzte Gemini-Storygenerationen wurden durch die neue Formal-QA abgelehnt; Gründe: zu knapper Handlungsabschnitt, zu wenige namentliche Hauptfiguren sowie fehlende genaue Angaben zu Rätselbildern/Rätseltyp.
- Statt fehlerhafte automatische Inhalte durchzuwinken, wurde Folge 001 als **redaktionell erstellter Pilot** gespeichert.
- Auto-Geschichtengenerator braucht weitere Prompt-/Modellkalibrierung, bevor tägliche Erzeugung als zuverlässig gelten kann.

## Sicherheit und Kosten
Keine öffentlichen TikTok-Posts oder kostenpflichtigen Upgrades aus der neuen Pipeline. Weiterhin separate Entwicklung von MOTUS. Nicht alle Video-Qualitätskontrollen sind bereits automatisiert; aktuell bremst das System fehlende Evidenz korrekt aus.
