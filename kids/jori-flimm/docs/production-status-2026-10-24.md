# Jori & Flimm – Produktionsstand 24.10.2026

Branch: `feature/jori-flimm-neustart-folge001`

## Veröffentlichungen und Planung

| Folge | Stand | Nachweis |
| --- | --- | --- |
| 001–003 | Buffer meldet veröffentlicht (`sent`) | [Live-Check, Run 40136219719](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40136219719) |
| 004 | `scheduled`, 25.10.2026, 14:00 Europe/Berlin | Buffer-Post `6ad9d34aaefa17e341fad444` |
| 005 | `scheduled`, 26.10.2026, 14:00 Europe/Berlin | Buffer-Post `6ad9d373e6aee73a2b15d107` |
| 006 – Der Ton im Glashaus | `scheduled`, 27.10.2026, 14:00 Europe/Berlin | Buffer-Post `6add2bd3e4be8a4d867c532c`; tatsächliche Buffer-Antwort: `status=scheduled`, `channelId=6ad948ea778b240e2f839607`, `dueAt=2026-10-27T13:00:00.000Z` (14:00 CET) |

Der Buffer-Read-only-Check bestätigte vor der Buchung den Kanal `@jori.flimm`, die unveränderten Termine für 004/005 und den freien 27.10.-Slot. Der separate Release-Lauf prüfte danach die echte MP4 und protokollierte die obigen Felder aus der Buffer-Antwort: [Folge-006-Release, Run 40137063992](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40137063992). Die Planung ist bestätigt; eine spätere TikTok-Veröffentlichung wird erst mit tatsächlichem Buffer-/TikTok-Nachweis als erfolgt gemeldet.

Folge 006 blieb unverändert. Tamás hat den etwa 2–3 Sekunden vorauseilenden Schlussuntertitel geprüft und ausdrücklich für die Veröffentlichung akzeptiert.

## Folge 007 – Der zweite Stern am Spiegelsee

- Die Geschichte setzt am zweiten passenden Stern aus Folge 006 ein und führt Jori und Flimm vom Glashaus zum Spiegelsee.
- Sechs eigens für diese Folge erzeugte, unterschiedliche 9:16-Szenenbilder liegen unter `kids/jori-flimm/relaunch-v2/assets/episode-007-v1/`. Jori behält ihre roten Mütze/Schal und den grünen Mantel; Flimm bleibt das runde goldene Wesen mit kleiner brauner Nase, grüner Mütze samt rotem Bommel und Stern auf dem Bauch.
- Sulafat-TTS lief mit dem freigegebenen Free-Tier-Modell `gemini-3.8-flash-lite-tts`; kein Paid-/Batch-/Flex-/Priority-Tarif und keine Bild-API wurden verwendet.
- Die echte MP4 ist 134,32 Sekunden lang, 720×1280 (9:16), H.264/AAC, 6.311.429 Bytes. Die sechs Bilddateien waren im Render-Workflow SHA-256-eindeutig.
- Der Rätselabschnitt zeigt Frage, Zielanordnung und alle drei Tafeln während der Denkpause. Der Audiotrack enthält dort genau 7,000 Sekunden digitale Stille; FFmpeg maß in der AAC-MP4 7,100 Sekunden. Währenddessen liegt kein Untertitel über der Stille; Lösung und neuer Cliffhanger folgen direkt danach.
- Untertitel-Wortfolge stimmt vollständig mit den fünf gesprochenen Sulafat-Segmenten überein. Die Bildwechsel sitzen an den tatsächlichen Segmentgrenzen: Teleskopbeobachtung, Weg zum See, Rätsel am Ufer, Lösung/Mira und dritter Stern.

**MP4 zur Sichtprüfung:** [Folge 007 auf GitHub](https://github.com/TamasHuettenheber/Motus-autamation/blob/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-28-e007-v1.mp4)

**Action-Nachweis:** [Folge-007-Render und MP4-QC, Run 40137063904](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40137063904) – erfolgreich; die QC-Ausgabe enthält Dauer, Codecs, Bildformat, Caption-Token-Abgleich und gemessene Stille.

Folge 007 bleibt eine Vorschau und wurde nicht zu Buffer geschickt. Veröffentlichung erst nach Tamás' Sichtprüfung/Freigabe.
