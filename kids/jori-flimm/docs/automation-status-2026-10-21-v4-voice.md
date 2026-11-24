# Jori & Flimm – QA-Übergabe V4, 21.10.2026

## Anlass
Nutzerfeedback: Folge 002 sprach viel zu leise, wirkte zu stark auf den Igel statt auf Flimm fokussiert, und die Victoria-Sprecherin klang österreichisch. Verbesserung vor Kanalstart verpflichtend.

## Umsetzung
1. **Text**: `episodes/jori-flimm-2026-10-22-e002.json` und `fixtures/e002-draft-2026-10-22.json` überarbeitet. Kein Igel mehr in der Sprecherhandlung, Jori und Flimm sind gemeinsam Hauptfiguren; Flimm entdeckt selbst die Sternenglocke. Unveröffentlichte Testfolge.
2. **Stimme**: `scripts/generate_voice_piper.py` ergänzt, deutscher Offline-TTS-Motor Piper, Stimme `de_DE-kerstin-low` (Deutsch / CC0-Sprachdaten, Pip/Piper-Abhängigkeiten für künftige öffentliche Nutzung gesondert auf Lizenz- und Plattformauflagen prüfen). Die bisherige Victoria bleibt nur als Legacy-Testoption vorhanden, wird bei neu kompilierten Testentwürfen nicht mehr gewählt. Sprecherprofil in `scripts/compile_preview_episode.py` umgestellt.
3. **Lautstärke**: `.github/workflows/kids-render.yml` normalisiert die finale Sprachspur mit EBU-R128-`loudnorm` auf Ziel `-16 LUFS, -1.5 dBTP`; zusätzliche Messung und QC-Gate `-18 bis -13.5 LUFS`.
4. **Kontrolle**: automatische Hauptfiguren-Prüfung in `scripts/generate_daily_story.py`. Neue Regressionstests `scripts/test_episode002_feedback.py`, insgesamt **14 von 14 Tests erfolgreich** (Actions Run [39682393995](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39682393995)).

## Echter Render-Test
- GitHub Actions Run **[39681377212](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39681377212)**: Status `success`, einschließlich TTS, Untertitel, MP4-Rendering, QC, Artefakt.
- Artefakt: `jori-flimm-2026-10-22-e002`, ID **12384886238**.
- Testdatei: `Jori_Flimm_Folge_002_Hochdeutsch_Lauter_V2.mp4`, **72,615 Sekunden**, 1080×1920, H.264/AAC.
- Lautheitsmessung vorher: **−25,48 LUFS**, True Peak −7,83 dBTP.
- Lautheitsmessung neue Testfassung: **−16,51 LUFS**, True Peak −1,33 dBTP; Differenz ca. +8,97 LU.
- Sechs Stichprobenbilder geprüft: Jori und Flimm auf Bildern sichtbar, Untertitel vorhanden. Drei Glocken werden visuell weiterhin nicht zuverlässig gezeigt. **Inhaltliche / bildbezogene Freigabe fehlt.**
- Neue Sprecherin ist ein de_DE-Modell, ihr Klang muss **vom Nutzer** bewertet werden. Keine objektive Garantie, dass der Dialekt zu 100 % neutral klingt.
- Testvideo in persönlicher ChatGPT-Bibliothek archiviert: `/Jori & Flimm/Testfolgen/Jori_Flimm_Folge_002_Hochdeutsch_Lauter_V2.mp4`.
- **Nicht veröffentlicht**: `preview_only: true`, 3 QC-Gates weiterhin false, Serien-/Folgenledger nicht fortgeschrieben. MOTUS nicht geändert.

## Nächste Schritte
1. Nutzer hört neue Sprachprobe auf mobilem Gerät, beurteilt Natürlichkeit und Neutralität.
2. Motivgetreue Bilder mit drei sichtbaren Glocken und Flimms Stern erstellen.
3. Nach bildlicher Kontrolle neu rendern und dann echten 7-Tage-Test der Produktionskette durchführen.
4. Zweites TikTok-Konto getrennt von MOTUS verbinden; Veröffentlichung um 14 Uhr erst nach gesonderter Freigabe und echtem Status-Test.

## Kosten
Keine zusätzliche bezahlte Verpflichtung; Open-Source-Piper-Engine und offizielle Sprachdatei sowie GitHub Actions auf öffentlichem Repository eingesetzt. Externe Lizenzbedingungen vor kommerzieller Verwendung separat prüfen.
