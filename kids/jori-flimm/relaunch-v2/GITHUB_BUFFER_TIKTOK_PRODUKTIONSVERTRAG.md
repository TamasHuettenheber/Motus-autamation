# Jori & Flimm – verbindliche GitHub → Buffer → TikTok Produktionsarchitektur
Stand: 22.10.2026. Nutzer hat ausdrücklich bestätigt, dass **GitHub das Video rendern und an Buffer übergeben** soll, wie bei MOTUS. Metricool gehört nicht in diese Pipeline.

## Freigabe und Istzustand
- **Folge 001 V10** ist die vom Nutzer ausdrücklich freigegebene Bild-/Ton-/Rätsel-Grundversion. Dateiname: `Jori_Flimm_Folge_001_V10_Ihren_Namen_Prueffassung.mp4`, SHA256 noch zu ermitteln.
- Die V10 wurde bei der iterativen Korrektur **lokal** statt im GitHub-Runner gerendert und in die ChatGPT-Bibliothek gesichert. **Dies war eine Abweichung vom beauftragten Produktionsweg und ist keine automatisierte GitHub-Produktion.**
- Der Branch enthält Storys, Bildquellen, Qualitätsregeln und eine Buffer-Read-only-Verbindung. Der bestehende Kids-Renderer (`.github/workflows/kids-render.yml`) ist auf den alten isolierten Branch `feature/jori-flimm-kids-pipeline` ausgelegt und entspricht nicht der freigegebenen V10-Renderlogik. Der Relaunch-Rolling-Workflow produziert **nur Entwürfe**, keine MP4 und keine Buffer-Posts.
- MOTUS: `.github/workflows/motus.yml` rendert im Runner, committed MP4 unter `published/` auf `main`, prüft öffentliches `raw.githubusercontent.com`-Video und bucht danach in Buffer. Diese **Reihenfolge** soll Jori übernehmen, aber mit strikt separatem Kanal @jori.flimm und eigenen Dateinamen.

## Sollzustand und verpflichtende Gates
1. Pro Episode Story/Payload mit lückenloser Fortsetzung des vorherigen Cliffhangers, Jori ist ein Mädchen (sie/ihr).
2. GitHub Actions bezieht Figurenbilder, Sprecherstimme Sulafat und die Rätselgrafik aus reproduzierbaren, versionierten Quellen. Für Folge 001 müssen die lokal verwendeten V10-Renderquellen/Skripte auf GitHub überführt werden; keine unkontrollierte visuelle Neufassung.
3. GitHub Actions rendert MP4 720×1280 oder besser H.264/AAC, mit sicheren, lesbaren Untertiteln, unverdeckten Bildern und **7 Sekunden echter Rätsel-Stille**.
4. Automatischer QC-Block: Pronomen, Untertitel-/Audio-Abgleich, Ton, sichtbare Rätselobjekte, Pause, Anschluss zur Vorfolge, identischer Render bei erneutem Lauf, manuelle Erstabnahme. Bei Fehler **kein Post**.
5. Erst danach commit nach `published/jori-flimm-YYYY-MM-DD-eNNN.mp4` in einem dafür freigegebenen GitHub-Branch, sodass Buffer die MP4 per **öffentlicher HTTPS-Raw-URL** laden kann. Keine Überschreibung von MOTUS-Dateien.
6. Buffer-API bucht genau **einen** Beitrag pro Folge am gewünschten Tag um **14:00 Europe/Berlin** auf dem per Handle geprüften TikTok-Kanal **jori.flimm**, mit Duplikatschutz. TikTok-/Buffer-Status und Post-ID erst nach echter Rückmeldung als gebucht melden.
7. Folgende Episoden laufen mit denselben GitHub-Actions-Schritten, statt erneut im Chat lokal zu rendern. Der lokale Bibliotheksordner bleibt ausschließlich **Backup/Review**, niemals Publishing-Quelle.

## Fehlende tatsächliche Umsetzung
- V10-Renderquellen/Skripte sind derzeit noch nicht vollständig in GitHub integriert.
- Es gibt noch **keinen erfolgreich gelaufenen GitHub-V10-Render-Job**, **keine veröffentlichte GitHub-V10-MP4-URL**, **keine Buffer-Post-ID**.
- Deshalb **nicht** behaupten, Folge 001 sei bereits für 14:00 eingeplant oder veröffentlicht. Ein Workflow, der nur Text-/Story-QC prüft, ist kein Publikationsnachweis.

Keine Kostenfreigabe, keine MOTUS-Änderungen.
