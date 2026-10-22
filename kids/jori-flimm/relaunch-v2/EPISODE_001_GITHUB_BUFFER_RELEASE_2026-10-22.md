# Jori & Flimm – Folge 001 – GitHub → Buffer Übergabe
Stand 22.10.2026, 10:50 Uhr MESZ.

## Erfolgreich abgeschlossen
- Isolierter GitHub-Workflow: `.github/workflows/jori-v10-github-buffer.yml`.
- Letzter erfolgreicher GitHub-Actions-Run: https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39750023764
- GitHub rendert Folge 001 aus versionierten Bildquellen und den Sulafat-Audio-Artefakten. Technisch geprüft: 104,28 Sekunden, H.264/AAC, MP4. Die GitHub-Rekonstruktion entspricht der V10-Geschichte und dem Stil; sie ist **keine byte-identische Kopie** der lokalen freigegebenen V10.
- Öffentliche MP4-Quelle: https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-22-e001.mp4
- Buffer hat die **alte Erstbuchung gelöscht** und die neu gerenderte Version bestätigt:
  - Buffer-Post-ID: `6ad9ce4baefa17e341f96c3f`
  - TikTok-Channel-ID: `6ad948ea778b240e2f839607`, Handle **@jori.flimm** im Workflow exakt geprüft.
  - Status: `scheduled`
  - `dueAt=2026-10-22T12:00:00.000Z` = **22.10.2026, 14:00 Uhr Europe/Berlin**.
  - Asset `mimeType=video/mp4`, Quelle siehe oben.
- MOTUS wurde nicht bearbeitet. Metricool wurde nicht verwendet.

## Noch nicht als Tatsache behaupten
- Der TikTok-Beitrag ist vor 14:00 Uhr **noch nicht veröffentlicht**. Buffer bestätigt die Planung, nicht die erfolgreiche TikTok-Publikation.
- Kein unabhängiger TikTok-Livecheck nach 14:00 Uhr durchgeführt.
- Die Pipeline ist derzeit für Folge 001 eingerichtet; tägliche Folge-002+-Automation ist noch nicht produktiv.

## Technische Abweichungen / Review
- Der Render-Workflow baut die lokal freigegebene V10 auf GitHub mit den ursprünglichen Quellen nach. Die neu gerenderte MP4 ist nicht binär identisch zur Bibliotheksfassung.
- Die Original-TTS-Erzählung aus Folge 001 ist unverändert; Untertitelkorrektur bei Joris weiblichem Pronomen erfolgt im GitHub-Renderer. Künftige Folgen sollen diese Inkonsistenz in der Stimme vermeiden.
