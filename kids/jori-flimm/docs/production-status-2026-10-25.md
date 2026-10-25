# Jori & Flimm – Produktionsstand 25.10.2026

Branch: `feature/jori-flimm-neustart-folge001`

## Buffer-Stand

| Folge | Status | Termin Europe/Berlin | Buffer-Post-ID |
| --- | --- | --- | --- |
| 001–003 | `sent` | 22.–24.10.2026 | laut Live-Check |
| 004 | `scheduled` | 25.10.2026, 14:00 | `6ad9d34aaefa17e341fad444` |
| 005 | `scheduled` | 26.10.2026, 14:00 | `6ad9d373e6aee73a2b15d107` |
| 006 – Der Ton im Glashaus | `scheduled` | 27.10.2026, 14:00 | `6add2bd3e4be8a4d867c532c` |
| 007 – Der zweite Stern am Spiegelsee | `scheduled` | 28.10.2026, 14:00 | `6addb8ddbd33ce99c3602edf` |

Vor der Buchung bestätigte der Read-only-Livecheck den separaten Kanal `@jori.flimm`, drei geplante Posts für den 25., 26. und 27.10. und keinen Folge-007-Post. Die tatsächliche Buffer-Antwort für Folge 007 lautet: `status=scheduled`, `channelId=6ad948ea778b240e2f839607`, `dueAt=2026-10-28T13:00:00.000Z` (14:00 MEZ). [Live-Check, Run 40175221956](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40175221956) · [Release mit Buffer-Bestätigung, Run 40175332068](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40175332068).

Die Einplanung ist bestätigt; eine Veröffentlichung auf TikTok wird erst nach einem tatsächlichen `sent`-/TikTok-Nachweis als erfolgt gemeldet.

## Folge 006 – Der Ton im Glashaus

Tamás hat die etwa 2–3 Sekunden vorauseilenden Schlussuntertitel ausdrücklich akzeptiert. Die geprüfte MP4 blieb unverändert und wurde für den 27.10. eingeplant. MP4-QC: 133,16 Sekunden, H.264 720×1280, AAC, gemessene Stille 7,105 Sekunden. [Folge-006-Buffer-Release](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40137063992).

## Folge 007 – Der zweite Stern am Spiegelsee

- Setzt am zweiten passenden Stern aus Folge 006 an und führt Jori und Flimm vom Glashaus zum Spiegelsee.
- Sechs eigens für Folge 007 generierte, unterschiedliche 9:16-Szenenbilder; Joris Pronomen sind weiblich, Flimm behält seine runde goldene Gestalt, die kleine Nase, die grüne Mütze mit rotem Bommel und den Bauchstern.
- Sulafat mit dem bestehenden Free-Tier-TTS-Modell; keine bezahlte Stufe und keine Gemini-Bild-API.
- Tatsächliche MP4: 134,32 Sekunden, H.264/AAC, 720×1280, 6.311.429 Bytes. Untertitel-Wortfolge stimmt mit den gesprochenen Segmenten überein; Szenenwechsel folgen den Audiosegmenten.
- Die WAV enthält exakt 7,000 Sekunden digitale Stille. Die fertige AAC-MP4 wurde mit 7,100 Sekunden gemessen. Frage und Hinweise bleiben während der Pause sichtbar; es gibt dort keinen Untertitel. Auflösung und neuer Cliffhanger folgen anschließend.
- [MP4 Folge 007](https://github.com/TamasHuettenheber/Motus-autamation/blob/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-28-e007-v1.mp4) · [Render- und MP4-QC, Run 40137063904](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40137063904)

Die erste Release-Ausführung wurde beim Stillecheck gestoppt, bevor Buffer aufgerufen wurde. Nach Korrektur des Prüfskripts bestand die tatsächliche MP4 den erneuten Check; nur der erfolgreiche Lauf 40175332068 legte den Post an. Es entstand kein zusätzlicher Buffer-Post.

## Folge 008 – Die Hüterin des dritten Sterns (Vorproduktion)

- Story und sechs neue, unterschiedliche 9:16-Szenenbilder liegen im Branch unter `relaunch-v2/episode_008_story_draft.json` und `assets/episode-008-v1/scene-01.png` bis `scene-06.png`. Der Einstieg greift den sinkenden dritten Stern und den Schatten aus Folge 007 direkt auf; das neue Rätsel führt zur Mondqualle und zum Gang in die versunkene Sternwarte.
- Veröffentlichung ist ausdrücklich gesperrt. Sulafat-TTS ist nicht erzeugt: in dieser Laufumgebung ließ sich der konkrete kostenlose Google-TTS-Tarif für das Projekt nicht nachweisen. Es gibt daher weder fertige MP4 noch geprüfte Audio-/Untertitel-Synchronität.
- Die neue Folge-008-Story-/Bild-Action führte die 28 bestehenden Unit-Tests erfolgreich aus. Der Folge-008-Gate-Test prüfte 28 Unit-Tests erfolgreich. Der Narrationsvergleich ignoriert jetzt PAUSE-/SEGMENT-Tags und normalisiert Zwischenräume, bevor er die gesprochene Wortfolge vergleicht; der korrigierte Lauf wird geprüft. [Action-Lauf](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40237234116).
- Der tatsächliche Buffer-Read-only-Check am 25.10.2026 bestätigt @jori.flimm, Folge 007 geplant für 28.10.2026 14:00 MEZ (Post `6addb8ddbd33ce99c3602edf`) und keinen Folge-008-Post. Der nächste freie Tages-Slot ist 29.10.2026, 14:00 MEZ; [Live-Check](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40237173440). Folge 008 wurde nicht an Buffer übergeben.
