# Jori & Flimm – Produktionsübergabe, 22.10.2026

## Live- und Planungsstatus

Die TikTok-Veröffentlichung von Folge 001 wurde geprüft: Buffer führt sie als „Post sent“ für `@jori.flimm` am 22.10.2026 um 14:00 Uhr (Europe/Berlin). Der öffentliche TikTok-Beitrag ist erreichbar unter [Folge 001 auf TikTok](https://www.tiktok.com/@jori.flimm/video/7699461062835309857).

Buffer zeigt im Jori-Kanal genau vier geplante Folgen 002–005. Titel, Uhrzeiten und Zeitzone stimmen. Es wurde keine Folge erneut angelegt.

| Folge | Titel | GitHub-Render | MP4 | Buffer | Termin Europe/Berlin | Buffer-Post-ID |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | Das Licht, das Joris Namen kannte | gerendert; lokale V10 vom Nutzer freigegeben, GitHub-Fassung technisch nicht dateiidentisch | [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-22-e001.mp4) | **veröffentlicht**; öffentlicher TikTok-Link bestätigt | 22.10.2026, 14:00 | `6ad9ce4baefa17e341f96c3f` |
| 002 | Drei Klopfzeichen im Laternenlicht | erfolgreich | [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-23-e002.mp4) | **scheduled** | 23.10.2026, 14:00 | `6ad9d2f9a013397d9328faea` |
| 003 | Die Tür, die niemand sehen konnte | erfolgreich | [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-24-e003.mp4) | **scheduled** | 24.10.2026, 14:00 | `6ad9d321a013397d932908dc` |
| 004 | Das falsche Schloss | erfolgreich | [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-25-e004.mp4) | **scheduled** | 25.10.2026, 14:00 | `6ad9d34aaefa17e341fad444` |
| 005 | Die Gestalt im Schneesturm | erfolgreich | [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-26-e005.mp4) | **scheduled** | 26.10.2026, 14:00 | `6ad9d373e6aee73a2b15d107` |

Folgen 002–005 wurden in GitHub Actions-Lauf [39753201500](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39753201500) produziert. Der Lauf protokolliert für jede Folge `JORI_EPISODE_RENDER_OK`, Sulafat-TTS und die bestätigte Buffer-Post-ID. Die GitHub-Rohdateien sind öffentlich abrufbar. Buffer-Status `scheduled` bestätigt die Planung; es ist noch kein Nachweis für die spätere TikTok-Veröffentlichung.

## Technischer Prüfbefund

- Alle vier MP4-Dateien sind mit ffprobe als H.264-Video in 720×1280 und AAC-Mono-Audio (24 kHz) erkannt worden. Containerlängen: E002 81,36 s; E003 79,08 s; E004 80,67 s; E005 79,16 s.
- Die Produktionslogs bestätigen Sulafat. Die Folgen setzen die vorherige Handlung fort: Laternenzeichen → verborgene Tür → Schlüssel und Schlösser → Gestalt im Schneesturm / Geheimnis von Flimms Stern. Es gibt keinen erneuten Einstieg oder ein neues Kennenlernen.
- Die korrigierte TTS-Erzeugung setzt Joris weibliche Pronomen für die bekannten fehlerhaften Stellen in E002 und E004 ein. Der erfolgreiche Renderlauf meldet für alle vier Folgen eine fertige Sulafat-Stimme.
- Die vorhandenen Illustrationen aus dem Jori-Bestand werden mit Folge-spezifischen Rätselkarten und Untertiteln kombiniert. Die visuellen Hintergründe wiederholen sich; eine eigenständige, beatgenaue Bildproduktion pro Folge liegt nicht vor.
- Untertitel werden satzweise nach Zeichenlänge über die Sprachsegmente verteilt. Eine ASR- oder wortgenaue Sprach-/Untertitel-Synchronisierung ist nicht nachgewiesen.
- Die TTS-Timeline enthält ein Rätsel-Pausensegment von 7 Sekunden. Eine unabhängige ffmpeg-Silence-Detektion auf den fertigen MP4s fand zusammenhängende Stille von 7,60 s (E002), 7,66 s (E003), 7,61 s (E004) und 7,71 s (E005) bei −25 dB. Damit ist die tatsächliche Frage-zu-Antwort-Pause nicht als exakt sieben Sekunden abgenommen; der Unterschied zur Timeline ist offen.
- Ein vollständiger menschlicher Hörtest, ein Mobilgeräte-Abspieltest sowie eine vollständige Sichtprüfung jedes Videos wurden nicht dokumentiert. Der technische Renderstatus ist daher keine vollständige redaktionelle Freigabe nach dem Regelwerk.

## Actions-Nachkontrolle und Wiederholungsschutz

Der spätere Lauf [39767338415](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39767338415) scheiterte vor dem Rendern von E003 beim Wiederherstellen eines älteren Audio-Artefakts (HTTP 401). Das verursachte keine zusätzliche Buffer-Planung; die schon geplanten Posts und MP4s blieben bestehen.

Am 22.10.2026 wurde `.github/workflows/jori-followups-fast.yml` angepasst: vorhandene MP4s auf dem Branch werden wiederverwendet, anstatt Sulafat erneut zu erzeugen oder die Folgen neu zu rendern. Vorhandene Buffer-Planungen werden weiterhin durch den Buffer-Duplikatschutz erkannt. Der Lauf [39818921335](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39818921335) prüft diese Änderung. **Sein Endstatus ist bei Erstellung dieses Dokuments noch offen und muss vor einem erfolgreichen Produktionsabschluss kontrolliert werden.**

## Tägliche Vorproduktion nach Folge 005

Das bestehende `.github/workflows/jori-relaunch-rolling-draft.yml` ist auf tägliche Story-Entwürfe um 20:00 Uhr Europe/Berlin angelegt. Es ist absichtlich deaktiviert, solange die Datei nicht auf dem Default-Branch liegt und `JORI_RELAUNCH_AUTO_DRAFTS` nicht aktiviert ist; außerdem würde es die externe Gemini-API aufrufen. Diese Freischaltungen wurden nicht vorgenommen.

Eine tägliche ChatGPT-Vorproduktionsautomation wurde angefordert, aber von der Automationsplattform abgelehnt: Kontingent ausgeschöpft (5 von 5 aktiven Aufgaben). Keine bestehende Aufgabe wurde verändert. Ohne freien Aufgabenplatz, oder eine gesondert autorisierte GitHub-Aktivierung mit möglicher API-Nutzung, läuft derzeit keine dauerhafte tägliche Vorproduktion.

Der nächste Story-Entwurf muss Folge 006 direkt beim riesigen Fußabdruck und dem Geheimnis von Flimms Stern beginnen. Entwürfe sind unveröffentlicht und unfreigegeben zu speichern. MOTUS blieb unverändert; Metricool wurde nicht verwendet.
