# Jori & Flimm – Produktionsstand 24.10.2026

Geprüft am 24.10.2026 um 20:05 Europe/Berlin auf Branch `feature/jori-flimm-neustart-folge001`.

## Veröffentlichungen und Queue

Die tatsächliche schreibgeschützte Buffer-Prüfung [GitHub Action 40119088145](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40119088145) bestätigte den TikTok-Kanal `@jori.flimm`, las die aktuellen Posts und nahm keine Änderungen vor.

| Folge | Titel | Buffer-Nachweis | Termin Europe/Berlin |
|---|---|---|---|
| 003 | Die Tür, die niemand sehen konnte | `sent`, Post `6ad9d321a013397d932908dc`; TikTok [Folge 003](https://tiktok.com/@jori.flimm/video/7700203623124389152) | 24.10.2026, 14:00; Buffer `sentAt 14:04:17` |
| 004 | Das falsche Schloss | `scheduled`, Post `6ad9d34aaefa17e341fad444` | 25.10.2026, 14:00 |
| 005 | Die Gestalt im Schneesturm | `scheduled`, Post `6ad9d373e6aee73a2b15d107` | 26.10.2026, 14:00 |
| 006 | Der Ton im Glashaus | Nicht in Buffer vorhanden | Nächster freier Tag: 27.10.2026, 14:00; nicht gebucht |

Die UTC-Zeit der bestätigten Posts ist 13:00Z am 25. und 26.10. Die Queue-Prüfung am 24.10. meldete nur Folge 004 und 005 als geplant; Folge 003 war tatsächlich gesendet. Folge 006 ist nicht doppelt vorhanden.

## Folge 006 – „Der Ton im Glashaus“

- **Kontinuität:** beginnt direkt beim riesigen Fußabdruck und Flimms Sterngeheimnis aus Folge 005. Jori bleibt durchgehend weiblich. Das Klangrätsel führt zur langen Glasröhre; die Auflösung erschließt Sternkarte und Teleskop; eine Gestalt mit einem zweiten Stern bildet den Cliffhanger.
- **Bilder:** fünf unterschiedliche, eigens für E006 erstellte 941×1672 Szenenbilder mit zum Glashaus, den Klangröhren, der Lösung und dem Cliffhanger passenden Hintergründen. Sichtprüfung repräsentativer Frames aus der fertigen MP4 bestanden. Das Rätselbild wird nach dem Rätselsegment entfernt.
- **Audio/Render:** GitHub Action [39999834452](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39999834452) erfolgreich; Sulafat; MP4 [Folge 006](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-27-e006.mp4). ffprobe: H.264/AAC, 720×1280, 131,76 s, 6.267.763 Bytes, Bild- und Tonspur vorhanden. Audio-Stille in der fertigen MP4 per ffmpeg gemessen: 7,139 s, innerhalb der erlaubten ±0,2 s. Die Frage/Hinweise bleiben im Pausenbild sichtbar; keine Untertitel überdecken die Pause.
- **Untertitel-QC: gesperrt.** Der Vergleich der Untertitel mit dem tatsächlichen Sprachtext findet sowohl heuristische Zeitmarken als auch fehlende Wörter/Abschnitte (u. a. „mittlere und eine lange“ und „Teleskop“). Damit sind die Untertitel weder vollständig noch sprachgenau. Die Datei bleibt Vorschau und wird nicht eingeplant. Erforderlicher nächster Schritt: Untertitel vollständig und am Sulafat-Audio ausgerichtet neu erzeugen, danach die vollständige MP4 erneut prüfen.
- **Kosten:** Es wurde in diesem Lauf kein TTS- oder Bild-API-Aufruf ausgelöst. Der bisherige E006-TTS-Lauf verwendete laut dokumentiertem Produktionsstand das vorhandene Modell `gemini-3.8-flash-lite-tts` im bestätigten Standard-Free-Tier; kein Tarifwechsel und keine Kostenverpflichtung. Die fünf E006-Bilder lagen bereits im Jori-Branch.

## Nächste Freigabe

Vor einer Buchung am 27.10. zuerst Untertitel am Sulafat-Audio ausrichten und MP4/Audio/Pause erneut prüfen; danach Buffer-Queue erneut read-only prüfen. MOTUS-Dateien und -Workflows blieben unberührt.
