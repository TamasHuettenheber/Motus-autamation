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

Folgen 002–005 wurden zunächst in GitHub Actions-Lauf [39753201500](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39753201500) produziert. Nach der Bildkorrektur wurden sie in Lauf [39825983006](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39825983006) mit je einer eigenen Folgeillustration neu gerendert. Der Lauf bestätigt die Laufzeiten per ffprobe und protokolliert für alle vier Folgen `JORI_BUFFER_POST_UPDATED_IN_PLACE`; dieselben Buffer-Post-IDs und Termine blieben erhalten. Die GitHub-Rohdateien sind öffentlich abrufbar. Buffer-Status `scheduled` bestätigt die Planung; es ist noch kein Nachweis für die spätere TikTok-Veröffentlichung.

## Technischer Prüfbefund

- Die neu gerenderten MP4s haben per ffprobe folgende Containerlängen und Dateigrößen: E002 80,766 s / 3.441.821 Byte; E003 78,406 s / 3.577.674 Byte; E004 80,028 s / 3.191.262 Byte; E005 78,482 s / 3.259.966 Byte. Der Renderer erzeugt 720×1280 H.264-Video und AAC-Mono-Audio mit 24 kHz. Die Laufzeitprüfung vergleicht Containerdauer und zusammengesetzte Audio-Timeline mit maximal 0,25 s Abweichung.
- Die Produktionslogs bestätigen Sulafat. Die Folgen setzen die vorherige Handlung fort: Laternenzeichen → verborgene Tür → Schlüssel und Schlösser → Gestalt im Schneesturm / Geheimnis von Flimms Stern. Es gibt keinen erneuten Einstieg oder ein neues Kennenlernen.
- Die korrigierte TTS-Erzeugung setzt Joris weibliche Pronomen für die bekannten fehlerhaften Stellen in E002 und E004 ein. Der erfolgreiche Renderlauf meldet für alle vier Folgen eine fertige Sulafat-Stimme.
- Für E002 bis E005 liegen jetzt vier eigenständige 9:16-Illustrationen in `kids/jori-flimm/assets/e002` bis `assets/e005`. Der Renderer lädt pro Folge ausschließlich deren `scene.jpg`; zwischen den Folgen werden keine Hintergründe wiederverwendet. Die Motive zeigen die jeweilige Handlung: Laternenfolge und Karte, verborgene Tür mit Zahlenreihe 2–4–6–?, Schloss-Truhe mit Formschlüsseln sowie Schneesturm mit Laternen und großem Fußabdruck. Joris Darstellung bleibt weiblich und über die Folgen konsistent.
- Untertitel werden satzweise nach Zeichenlänge über die Sprachsegmente verteilt. Eine ASR- oder wortgenaue Sprach-/Untertitel-Synchronisierung ist nicht nachgewiesen.
- Für die Bildkorrektur wurde keine neue TTS-Anfrage ausgelöst. Die Sulafat-Audiospur wurde aus den ursprünglichen GitHub-Versionen der MP4s wiederhergestellt; dabei erkannte ffmpeg Stille von 7,599 s (E002), 7,655 s (E003), 7,612 s (E004) und 7,708 s (E005). Der Renderer setzt daraus jeweils eine sieben Sekunden lange Pause zusammen. Die finalen Laufzeiten stimmen laut ffprobe mit der neu zusammengesetzten Audio-Timeline überein; eine separate Silence-Detektion nach dem AAC-Encoding ist nicht protokolliert.
- Ein vollständiger menschlicher Hörtest, ein Mobilgeräte-Abspieltest sowie eine vollständige Sichtprüfung jedes Videos wurden nicht dokumentiert. Der technische Renderstatus ist daher keine vollständige redaktionelle Freigabe nach dem Regelwerk.

## Actions-Nachkontrolle und Wiederholungsschutz

Der spätere Lauf [39767338415](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39767338415) scheiterte vor dem Rendern von E003 beim Wiederherstellen eines älteren Audio-Artefakts (HTTP 401). Das verursachte keine zusätzliche Buffer-Planung; die schon geplanten Posts und MP4s blieben bestehen.

Am 22.10.2026 wurde `.github/workflows/jori-followups-fast.yml` angepasst: vorhandene MP4s auf dem Branch werden wiederverwendet, anstatt Sulafat erneut zu erzeugen oder die Folgen neu zu rendern. Vorhandene Buffer-Planungen werden weiterhin durch den Buffer-Duplikatschutz erkannt. Der erste Prüflauf [39818921335](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39818921335) wurde während des langsamen `apt`-Downloads abgebrochen, bevor Folgen oder Posts verarbeitet wurden. Der Ersatzlauf [39819980226](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39819980226) endete **success**. Seine Logs belegen für E002–E005 `JORI_EXISTING_RENDER_REUSED` und `JORI_EPISODE_ALREADY_SCHEDULED` mit den vorhandenen Buffer-IDs; es wurde kein Duplikat angelegt. Weil alle MP4s vorhanden waren, entfiel die Werkzeuginstallation. Der optionale Actions-Artefakt-Upload meldete keine Dateien, da das sparse checkout den Ordner `published` nicht in den Runner-Arbeitsbereich übernimmt; die MP4s liegen weiterhin im Branch und die oben verlinkten öffentlichen GitHub-Dateien sind davon unabhängig.

## Tägliche Vorproduktion nach Folge 005

Das bestehende `.github/workflows/jori-relaunch-rolling-draft.yml` ist auf tägliche Story-Entwürfe um 20:00 Uhr Europe/Berlin angelegt. Es ist absichtlich deaktiviert, solange die Datei nicht auf dem Default-Branch liegt und `JORI_RELAUNCH_AUTO_DRAFTS` nicht aktiviert ist; außerdem würde es die externe Gemini-API aufrufen. Diese Freischaltungen wurden nicht vorgenommen.

Eine tägliche ChatGPT-Vorproduktionsautomation wurde angefordert, aber von der Automationsplattform abgelehnt: Kontingent ausgeschöpft (5 von 5 aktiven Aufgaben). Keine bestehende Aufgabe wurde verändert. Ohne freien Aufgabenplatz, oder eine gesondert autorisierte GitHub-Aktivierung mit möglicher API-Nutzung, läuft derzeit keine dauerhafte tägliche Vorproduktion.

Der nächste Story-Entwurf muss Folge 006 direkt beim riesigen Fußabdruck und dem Geheimnis von Flimms Stern beginnen. Entwürfe sind unveröffentlicht und unfreigegeben zu speichern. MOTUS blieb unverändert; Metricool wurde nicht verwendet.
