# Jori & Flimm – Produktionsstand 22.10.2026

## Ergebnis

Folgen 002–005 wurden über GitHub Actions mit je fünf folgenspezifischen Szenenbildern neu gerendert. Die Videos sind vertikal (720×1280, H.264/AAC), enthalten Sulafat-Audio, Untertitel und eine sieben Sekunden lange Rätselpause. Die Frage steht während der Pause auf der Rätselkarte; die vorherige Untertitelzeile läuft nicht weiter.

Die Stichproben der MP4s wurden bildlich geprüft. Zwischen Hook, Handlung, Rätsel, Auflösung und Cliffhanger wechseln die Szenen. Die Laternenfolge in Folge 002 zeigt Blau–Gold–Blau–Gold. Storytexte und sichtbare Zeile „sagte sie“ in Folge 004 verwenden Jori weiblich.

## Folgen und Veröffentlichung

| Folge | Titel | Render / GitHub-MP4 | Buffer | Termin Europe/Berlin | Buffer-Post-ID |
|---|---|---|---|---|---|
| 001 | Das Licht, das Joris Namen kannte | Vorhanden: [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-22-e001.mp4) | **sent**; Buffer meldet Versand um 14:02:53 CEST. TikTok-Link: https://tiktok.com/@jori.flimm/video/7699461062835309857 | 22.10.2026, 14:00 | `6ad9ce4baefa17e341f96c3f` |
| 002 | Drei Klopfzeichen im Laternenlicht | **success**, 80,766 s; [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-23-e002.mp4) | **scheduled** | 23.10.2026, 14:00 CEST | `6ad9d2f9a013397d9328faea` |
| 003 | Die Tür, die niemand sehen konnte | **success**, 78,406 s; [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-24-e003.mp4) | **scheduled** | 24.10.2026, 14:00 CEST | `6ad9d321a013397d932908dc` |
| 004 | Das falsche Schloss | **success**, 80,028 s; [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-25-e004.mp4) | **scheduled** | 25.10.2026, 14:00 CET | `6ad9d34aaefa17e341fad444` |
| 005 | Die Gestalt im Schneesturm | **success**, 78,458 s; [MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-26-e005.mp4) | **scheduled** | 26.10.2026, 14:00 CET | `6ad9d373e6aee73a2b15d107` |

Buffer bestätigte für alle vier Folgen den Kanal `@jori.flimm`. Ein erfolgreicher Folge-Lauf hat die vorhandenen MP4s wiederverwendet und alle vier bestehenden Posts als bereits geplant erkannt; es wurden keine Duplikate angelegt. Die UTC-Zeit wechselt am 25.10. wegen der Zeitumstellung von 12:00Z auf 13:00Z, jeweils 14:00 Uhr Ortszeit.

## Ausgeführte Kontrollen

- Erfolgreicher Bild-/Video-Refresh: GitHub Actions Run [39835201159](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39835201159).
- Idempotenz- und Buffer-Statusprüfung: Run [39836766944](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39836766944).
- Read-only-Prüfung des Jori-TikTok-Kanals und Versandstatus Folge 001: Run [39836845360](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39836845360). Buffer meldet Folge 001 als `sent` und liefert den oben genannten TikTok-Link.
- ffprobe bestätigte in allen vier MP4s Video und AAC-Audiospur im 9:16-Format. Silencedetect bestätigte die sieben Sekunden Pause (E003: 6,994 s).
- Der Rätselbildschirm zeigt während der Pause keine weiterlaufende Untertitelzeile. Die E002-Stichproben zeigen fünf unterschiedliche Szenen statt eines Hintergrunds über das ganze Video.

## Jori-Pronomen und TTS-Hinweis

Folge 004 enthielt im kanonischen Storytext einmal „sagte er“. Story und Narration in `staffel1_folgen_001_005.json` sind jetzt auf „sagte sie“ korrigiert. Die bestehende Sulafat-Aufnahme wurde zuvor erfolgreich aus dem korrigierten Text erzeugt (Run [39753201500](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39753201500)) und bei der Bildaktualisierung wiederverwendet. Ein einzelner späterer Neuaufbauversuch erhielt von Gemini HTTP 429, bevor MP4 oder Buffer-Post verändert wurden (Run [39836089743](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39836089743)); es wurde kein weiterer TTS-Retry ausgelöst.

## Tägliche Vorproduktion nach Folge 005

Der isolierte Workflow `.github/workflows/jori-relaunch-rolling-draft.yml` enthält eine tägliche Story-Vorproduktion um 20:00 Uhr Europe/Berlin. Er erstellt drei Tage vor dem Zieltermin einen **unveröffentlichten Story-Entwurf** auf dem Jori-Branch und erzeugt weder Video noch Buffer-/TikTok-Post.

Der Zeitplan ist derzeit **noch nicht aktiv**: GitHub führt `schedule`-Workflows nur aus, wenn die Workflow-Datei im Standard-Branch liegt; außerdem verlangt der Job die Repository-Variable `JORI_RELAUNCH_AUTO_DRAFTS=true`. Der aktuelle Arbeitszweig bleibt `feature/jori-flimm-neustart-folge001`. Eine Aktivierung wurde nicht vorgenommen, damit weder der Standard-Branch/MOTUS berührt noch ein laufender Gemini-API-Aufruf ohne bestätigte Kostenfreigabe ausgelöst wird. Manuelle `workflow_dispatch`-Vorbereitung bleibt auf dem Feature-Branch verfügbar.

MOTUS-Workflows und Metricool wurden nicht geändert bzw. verwendet.
