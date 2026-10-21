# Jori & Flimm – Übergabe V3 – 21. Oktober 2026

## Anlass
Nutzer meldet die Einrichtung eines Gemini-API-Schlüssels im GitHub-Actions-Secret `JORI_GEMINI_API_KEY` als abgeschlossen und beauftragt die Fortsetzung der technischen Tests.

## Tatsächlich geprüft
- GitHub Actions hat das Vorhandensein des Repository-Secrets bestätigt (`JORI_KEY_PRESENT`). Der Secret-Wert wurde weder ausgelesen noch in Logs ausgegeben.
- Ein **echter API-Aufruf mit Gemini 3.5 Flash-Lite** hat einen deutschsprachigen originalen Serienentwurf geliefert. Dies belegt funktionierende API-Autorisierung und Textgenerierung.
- Beim ersten Lauf [39679707021](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39679707021) wurde der Entwurf durch die QA gestoppt, da die Sprecherfrage nicht wortwörtlich dem Rätselfeld entsprach. Kein fehlerhafter Entwurf gespeichert.
- `kids/jori-flimm/scripts/generate_daily_story.py` wurde so erweitert, dass eine einzige begrenzte KI-Überarbeitung erfolgt, falls die formale Story-QA einen Fehler erkennt. Das Standardmodell ist jetzt `gemini-3.5-flash-lite`. Keine Endlosschleifen.
- Zweiter Workflowlauf [39679989817](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39679989817) **erfolgreich**.
- Ergebnis: `kids/jori-flimm/drafts/jori-flimm-2026-10-23-e003.json`, Episode 003, Titel **„Das Rätsel der Eiskristall-Brücke“**.
- Die Datei hat ausdrücklich `approved_for_publish: false` und `status: draft_requires_illustration_and_qc`. Es gibt noch keine Videos, Publikation, TikTok-Verbindung oder neuen offiziellen Serienstand.

## Grenzen / bevorstehende Aufgaben
1. Die Story-Anbindung wurde einmal erfolgreich unter GitHub Actions nachgewiesen. **Noch kein 7-Tage-Dauertest und keine aktivierte nächtliche Schedule.**
2. Formal-QA reicht nicht zur vollständigen visuellen oder erzählerischen Qualitätsprüfung. In Episode 003 beschreibt Bildszene 1 bereits die Lichtwerkstatt, obwohl die Handlung die Brücke davor zeigt; Bildbriefings müssen vor Videoerstellung narrativ geprüft und bei Bedarf korrigiert werden.
3. Automatische neue, motivgenaue Illustrationen sind weiterhin offen. Bestehende alte Montagebilder sind als reine Testvorschau geeignet, aber keine veröffentlichungsreifen neuen Episodenbilder.
4. TTS ist im isolierten Renderer technisch getestet, die öffentliche TTS-Demo ist nicht dauerhaft garantiert.
5. Ein eigener TikTok-Kanal samt offizieller Veröffentlichungsschnittstelle fehlt. Bestehender MOTUS-Kanal bleibt unangetastet.
6. GitHub-Schedule läuft nur nach Testfreigabe über den Standardzweig; kein Merge in `main` vorgenommen.
7. Gemini-Free-Tier ist offiziell vorhanden, aber der genaue Abrechnungsstatus des persönlichen Google-Projekts kann über GitHub Actions nicht verifiziert werden; keine bezahlten Upgrades oder neuen Abos angelegt.

## Nächster Schritt
- Ein eigenes illustriertes Testvideo mit zur Handlung passenden Bildern erstellen und einen vollständigen Render-/Hör-/Sichttest durchführen.
- Die Textproduktion sieben unabhängige Male samt Kontinuitätscheck laufen lassen; bei jeder QA-Ablehnung keine Veröffentlichung.
- Erst danach neuer TikTok-Kanal, Draft-Veröffentlichungstest und 14-Uhr-Publishing-Schedule.

## Sicherheit
- Änderungen ausschließlich auf `feature/jori-flimm-kids-pipeline` in PR #66.
- Keine MOTUS-Workflows umgestellt.
- GitHub-Secret nicht in Code, Artefakt oder Dokumenten ausgegeben.
- Der ältere, einmalige Testworkflow `.github/workflows/jori-gemini-once-20261021.yml` diente ausschließlich der kontrollierten Prüfung. Nicht als Dauer-Schedule verwenden.
