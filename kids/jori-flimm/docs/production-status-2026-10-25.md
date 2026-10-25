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

## Folge 008 – Die Hüterin des dritten Sterns

- Die Story knüpft direkt an den dritten sinkenden Stern und den Schatten aus Folge 007 an. Das Rätsel führt zur Mondqualle und öffnet den Weg zur versunkenen Sternwarte.
- **Free-Tier-Nachweis:** Folge 007 wurde erfolgreich mit Sulafat über `gemini-3.8-flash-lite-tts` gerendert. Die [Action 40137063904](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40137063904) bezeichnet den Schritt ausdrücklich als Free-Tier-Modell und weist die erfolgreiche Sulafat-Ausgabe aus. Folge 008 nutzte denselben Modell-/Voice-Pfad; kein Modell-, Tarif- oder Billing-Wechsel.
- Sechs neu generierte, unterschiedliche Szenenbilder liegen unter `assets/episode-008-v1/scene-01.png` bis `scene-06.png`. Story-, Pronomen-, Bild- und Python-Checks bestanden. Flimm behält seine goldene Form, den kleinen Nasenpunkt, Bauchstern und die grüne Mütze.
- Die fertige [GitHub-MP4](https://github.com/TamasHuettenheber/Motus-autamation/blob/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-29-e008-v1.mp4) wurde tatsächlich geprüft: 133,833 Sekunden, H.264 720×1280, AAC, 6.256.059 Bytes. Die WAV enthält sieben Sekunden digitale Stille; in der MP4 wurden 7,053 Sekunden gemessen. Rätsel-Frage und alle Hinweise sind während der Stille sichtbar; danach wechselt das Bild zur Auflösung. Untertitel-Wortfolge stimmt mit den gesprochenen Segmenten überein, und es gibt keine Untertitel in der Stille. Stichproben aus allen sechs Szenen passen zum jeweiligen Handlungsteil.
- [E008-Render-/QC-Action](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40242318584). Der aktuelle Buffer-Read-only-Check bestätigt @jori.flimm und keinen E008-Post; [Live-Check 40242649128](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40242649128). Folge 006 bleibt am 27.10. und Folge 007 am 28.10., beide 14:00 Uhr geplant. Folge 008 ist über GitHub → Buffer für 29.10.2026, 14:00 Uhr MEZ eingeplant: `status=scheduled`, Post-ID `6ade8a490b5343d070f6b831`, Kanal-ID `6ad948ea778b240e2f839607`, `dueAt=2026-10-29T13:00:00.000Z`. Die tatsächliche Buffer-Antwort stammt aus [Release-Run 40242786784](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40242786784); der anschließende [Read-only-Livecheck 40242892798](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40242892798) bestätigt denselben Post. Der [idempotente Kontrolllauf 40242931491](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40242931491) erkannte ihn als bereits geplant und erzeugte keinen Duplikatpost. Noch keine Veröffentlichung behauptet: Buffer zeigt `scheduled`, nicht `sent`.
