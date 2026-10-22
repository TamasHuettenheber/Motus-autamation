# Jori & Flimm – aktualisierter Veröffentlichungskalender, 22. Oktober 2026

## Nutzerfreigabe für den gewünschten Start
Der Nutzer hat den bisher vorgesehenen Start am 23. Oktober ausdrücklich auf **heute, Donnerstag 22. Oktober 2026 um 14:00 Uhr Europe/Berlin** vorgezogen. **Genau ein Video pro Tag**, niemals alle fünf am selben Tag.

| Folge | Tag | Veröffentlichungsziel lokal | Geplanter UTC-Zeitpunkt | Tatsächliche Buffer-Buchung |
|---:|---|---|---|---|
| 001 | Donnerstag, 22.10. | 14:00 CEST | 2026-10-22T12:00:00Z | NOCH NICHT GEBUCHT |
| 002 | Freitag, 23.10. | 14:00 CEST | 2026-10-23T12:00:00Z | NOCH NICHT GEBUCHT |
| 003 | Samstag, 24.10. | 14:00 CEST | 2026-10-24T12:00:00Z | NOCH NICHT GEBUCHT |
| 004 | Sonntag, 25.10. | 14:00 CET | 2026-10-25T13:00:00Z | NOCH NICHT GEBUCHT |
| 005 | Montag, 26.10. | 14:00 CET | 2026-10-26T13:00:00Z | NOCH NICHT GEBUCHT |
| 006 | Dienstag, 27.10. | 14:00 CET | 2026-10-27T13:00:00Z | Noch kein freigegebenes Video |
| 007 | Mittwoch, 28.10. | 14:00 CET | 2026-10-28T13:00:00Z | Noch kein freigegebenes Video |
| 008 | Donnerstag, 29.10. | 14:00 CET | 2026-10-29T13:00:00Z | Noch kein freigegebenes Video |

Am 25.10.2026 endet die Sommerzeit. Lokal bleibt es immer 14 Uhr; UTC springt von 12 Uhr auf 13 Uhr.

## Technische Änderung in GitHub (erledigt und getestet)
- `relaunch-v2/scripts/rolling_calendar.py`: FIRST=2026-10-22; anschließend täglich 14:00 Europe/Berlin.
- `relaunch-v2/buffer_folgen_001_005_entwuerfe.json`: alle fünf Zieldaten und UTC-Termine um einen Tag vorgezogen; ausdrücklich **scheduled_in_buffer=false**.
- `relaunch-v2/scripts/test_rolling_calendar.py`: fünf Termine, Zeitumstellung, Vorsprung und Doppelbelegungs-Schutz aktualisiert.
- `relaunch-v2/scripts/generate_episode.py`: bestehende Handlungen 001–005 auf 22.–26. Okt. umdatiert, damit die automatische Fortsetzung für 27. Oktober **Episode 006** erzeugt statt Episode 005 oder einen falschen Doppelentwurf.
- `.github/workflows/jori-relaunch-quality.yml` erwartet im Dry-run nächste `e006` für den 27.10.
- Die Code- und Regressionstests sind erfolgreich gelaufen. Dies **bestätigt keine tatsächliche Veröffentlichung**.

## Rollierende Produktion ab Episode 006
Mit einem dreitägigen Vorlauf sollen die nächsten Folgen erstellt werden:
- Folge 006, Veröffentlichung Di. 27.10.: Produktionsstart **Sa. 24.10. 20:00 CEST**.
- Folge 007, Veröffentlichung Mi. 28.10.: Produktionsstart **So. 25.10. 20:00 CET**.
- Folge 008, Veröffentlichung Do. 29.10.: Produktionsstart **Mo. 26.10. 20:00 CET**.
- 20:30: sechs individuell passende Illustrationen, einheitliche Sulafat-Vertonung, Video.
- 21:30: Qualitätsprüfungen von tatsächlicher Sprache, synchronisierten Untertiteln, originalen Rätselobjekten und Handlung, sieben Sekunden Stille, natürlichem Cliffhanger, finalem Ton.
- Spätestens 19:00 am Vortag soll eine **final QC-FREIGEGEBENE** MP4 mit stabiler HTTPS-URL im Buffer für genau einen Tag um 14 Uhr fest eingeplant sein.
- Produktionsvorrat: ideal mindestens 3 fertige und gebuchte Folgen.

## Sofortige Hinderungsgründe zur Veröffentlichung um 14:00 HEUTE
1. Die fünf vorhandenen Video-MP4 sind Arbeitsfassungen, noch keine redaktionell endgültig freigegebenen Fassungen; konkret fehlt vollständige übereinstimmende Schrift-Sprache-Synchronisierung, motivtreue Einzelillustrationen und Handy-Hörprüfung. Beim Sichttest am 22.10. zeigte Folge 001 zwar Mond/Sonne/Stern korrekt an, aber auch bestehende Hintergrundmotive statt vollständig individueller Bildszenen; kein vollständiger Untertitel-Abgleich.
2. Laut Buffer API-Dokumentation muss für ein Videoposting die Medien-URL öffentlich ohne Anmeldung erreichbar sein **bis die Veröffentlichung stattfindet**. ChatGPT-Library- und herunterladbare Actions-Artefaktlinks sind nicht automatisch geeignete dauerhafte öffentliche HTTPS-Medien-URLs.
3. Am 22.10. war der Buffer-Kanal @jori.flimm über bereits vorhandenen `BUFFER_API_KEY` bestätigt; zu dem Zeitpunkt **0 geplante Posts**.
4. Keine tatsächliche Buffer-Post-ID für Folge 001–005, daher **KEINE Veröffentlichung behaupten**. Auch keine stumme oder nur Text-Alternative anstelle der Geschichte veröffentlichen.
5. GitHub-Zeitsteuerung zur laufenden Erstellung ist lediglich vorbereitet, deaktiviert bis nach unabhängiger Qualitäts- und Kanalprüfung.

## Freigaberegel
Nur der verifizierte TikTok-Kanal @jori.flimm. MOTUS niemals ändern. Keine kostenpflichtigen Tarif-Upgrades. Videos erst nach bestandener Pflicht-QC, funktionierender Direktmedien-URL, korrekt datierter Buffer-Post-ID und später tatsächlicher TikTok-URL als gebucht/veröffentlicht melden.

**Die Nutzerbitte nach 14 Uhr heute wird als Ziel dokumentiert, nicht als Erfolg behauptet.** Es darf nicht versehentlich unvollständiges oder anderes Material bloß zur Terminerfüllung veröffentlicht werden.
