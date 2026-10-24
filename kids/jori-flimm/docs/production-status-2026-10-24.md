# Jori & Flimm – Produktionsstand 24.10.2026

Geprüft am 24.10.2026 um 20:27 Europe/Berlin auf Branch `feature/jori-flimm-neustart-folge001`.

## Veröffentlichungen und Queue

Die schreibgeschützte Buffer-Prüfung [GitHub Action 40119088145](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40119088145) bestätigte den TikTok-Kanal `@jori.flimm` und las die tatsächlichen Posts, ohne etwas zu ändern.

| Folge | Titel | Buffer-Nachweis | Termin Europe/Berlin |
|---|---|---|---|
| 003 | Die Tür, die niemand sehen konnte | `sent`, Post `6ad9d321a013397d932908dc`; TikTok [Folge 003](https://tiktok.com/@jori.flimm/video/7700203623124389152) | 24.10.2026, 14:00; Buffer meldet Versand 14:04:17 |
| 004 | Das falsche Schloss | `scheduled`, Post `6ad9d34aaefa17e341fad444` | 25.10.2026, 14:00 |
| 005 | Die Gestalt im Schneesturm | `scheduled`, Post `6ad9d373e6aee73a2b15d107` | 26.10.2026, 14:00 |
| 006 | Der Ton im Glashaus | Nicht in Buffer vorhanden | Nächster freier Tag: 27.10.2026, 14:00; nicht gebucht |

## Folge 006 – „Der Ton im Glashaus“, korrigierte Vorschau v2

Tamás meldete, dass die Glashausbilder erschienen, während die Erzählung noch am Fußabdruck war, und dass Flimm anders aussah. **Er hat nichts verpasst:** In v1 waren breite Erzählteile zu wenigen Standbildern zusammengefasst; die neu erzeugten Bilder waren nicht ausreichend an Folge 005 als Figurenreferenz gebunden. Dadurch drifteten Szenenreihenfolge und Flimms Aussehen.

- **Korrektur:** sechs neue, unterschiedliche Szenenbilder nach Folge 005 als Referenz erzeugt und im Jori-Branch unter `relaunch-v2/assets/episode-006-v2/` abgelegt. Flimm ist wieder rund, golden, mit der kleinen Nase, grüner Mütze und sichtbarem Stern am Bauch. Jori bleibt dieselbe Figur mit roter Mütze.
- **Szenenfolge geprüft:** 12 s – Fußabdruck/Nachricht; 26 s – der silberne Faden führt zum Glashaus; 33 s – Eintritt und Innenraum mit den Glasröhren. Lösung/Teleskop und Gestalt mit zweitem Stern folgen anschließend. Die Rätselkarte ist nur während Frage und Denkpause eingeblendet.
- **Story-/Bild- und Render-Action** [40120500381](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40120500381) erfolgreich; Story-/Pronomen-QC und sechs unterschiedliche 720×1280 Bilder bestanden. Sulafat-TTS lief im vorhandenen bestätigten Standard-Free-Tier; kein Paid-/Batch-/Flex-/Priority-Modus und keine Tarifänderung.
- **Fertige MP4 v2:** [Folge 006 ansehen](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-27-e006-v2.mp4). Tatsächliche MP4: H.264/AAC, 720×1280, 133,16 s, 6.046.272 Bytes. FFmpeg misst 7,105 s Stille in der AAC-Datei; das liegt innerhalb der erlaubten ±0,2 s.
- **Untertitel:** Wortlautabgleich mit der tatsächlichen Sulafat-Textspur bestanden (243/243 Wörter); kein Untertitel läuft in die Rätselpause hinein. Die Satz-/Zeilenzeitmarken werden aber weiterhin proportional nach Textlänge geschätzt statt sprachbasiert ausgerichtet. Deshalb bleibt v2 eine **Vorschau**, ohne Buffer-Buchung. Ein physischer iPhone-Abspieltest liegt nicht vor.

## Nächster Freigabeschritt

Die korrigierte Vorschau ansehen; vor jeder Buchung die Untertitel zeitlich am Sulafat-Audio ausrichten, die MP4 erneut prüfen und Buffer live read-only auf Kanal, Folge und Termin kontrollieren. MOTUS-Dateien und -Workflows blieben unberührt.
