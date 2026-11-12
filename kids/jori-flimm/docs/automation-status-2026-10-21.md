# Jori & Flimm – GitHub-Automation, Übergabestand 2026-10-21

## Ziel
Jeden Tag eine NEUE, eigenständige Folge für die Serie verfassen und für eine gesonderte Veröffentlichung **um 14:00 Uhr Europe/Berlin** vorbereiten. MOTUS bleibt unabhängig mit seinen vier bisherigen täglichen Videos.

## Stand: in GitHub umgesetzt
- Eigener Entwicklungszweig: \`feature/jori-flimm-kids-pipeline\`, Pull Request #66 (Entwurf), **nicht** in \`main\` gemergt.
- Vorhandener Renderer: Jori-&-Flimm-Episode-000-Test aus GitHub Actions erfolgreich, ca. 84 Sekunden, vertikal H.264/AAC. Das ist nur eine technische Prüfung, kein bestandener 7-Tage-Dauertest.
- **Neu**: \`scripts/generate_daily_story.py\` mit kostenoptionalem, externem JSON-Textgenerator (Standard \`gemini-2.5-flash-lite\`) und Lesezugriff auf Serien-Bibel und Ledger. Prüft Folgenummer, exakte Titel-/Hook-/Rätselduplikate, eine echte 5–10-Sekunden-Denkpause sowie gesprochene Frage/Antwort. Kein Anspruch auf vollständige semantische, rechtliche oder pädagogische Inhaltsprüfung.
- Bis zu sieben unveröffentlichte Story-Entwürfe werden chronologisch fortgeschrieben, ohne den verbindlichen Serienstand voreilig als produziert zu markieren. Danach Sicherheitsstopp.
- **Neu**: \`.github/workflows/jori-flimm-daily-draft.yml\`: nächtlicher Entwurfszeitplan **22:17 Uhr Europe/Berlin** (Folge für den nächsten Tag); Offline-CI auf dem Entwicklungszweig; abgesicherter Live-Job nur bei Repo-Variable \`JORI_STORY_DRAFTS_ENABLED=true\`.
- Der GitHub-CI-Test darf ohne Textdienst, Login und Kosten laufen. Kein TikTok-Veröffentlichen, keine Änderungen an regulären MOTUS-Workflows.

## Warum noch nicht täglich live
1. GitHub-Schedule läuft nur vom **Standardzweig \`main\`**. Das neue Skript liegt absichtlich ausschließlich im isolierten Testzweig; ein Merge und das Aktivieren sind bewusst ausstehend.
2. Für die täglich neuen Geschichtentexte fehlt derzeit ein nachweislich verbundener API-Zugang. GitHub Models wurde zum 30.07.2026 eingestellt. Alternativ ist ein API-Schlüssel für **einen ausdrücklich kostenlosen, nicht abrechnenden** Textdienst vorgesehen; keine Schlüssel in Dateien ablegen. Niemals automatisiert die kostenpflichtige Stufe aktivieren.
3. Der neue Textgenerator produziert **Storyboards und Sprechertexte als nicht freigegebene Entwürfe**. Neue, passende Illustrationen zu jeder Folge sind technisch noch nicht autonom gesichert.
4. Vorhandene TTS-Voice über eine öffentliche CPU-Demo ist kein zugesicherter 24/7-Service; Tonqualität, Texttreue und Verfügbarkeit müssen täglich technisch geprüft werden.
5. Ein eigener Jori-&-Flimm-TikTok-Kanal bzw. dessen Buffer-Anbindung fehlt. Unabhängiger Kanal und ausdrücklich dazugehöriger Publish-Zugang müssen einmalig vom Kontoinhaber autorisiert werden.
6. GitHub kann eine Veröffentlichung für 14:00 vorplanen und Status kontrollieren; ob TikTok diese tatsächlich sendet, ist erst nach erfolgreichem End-to-End-Test belegbar.

## Sichere Reihenfolge für Fortsetzung
1. Offline-CI und einen einzelnen externen Entwurfs-Lauf **ohne Kosten** nach Freigabe des Free-Tier-Zugangs prüfen.
2. Sieben originelle, zum Kanon passende Entwürfe über sieben Tage erstellen; Text-/Rätselduplikate und rote Fäden vergleichen.
3. Für neue Folgen passenden eigenen Bildaufbau und die Erzählerstimme sichern; exakte Story/Audio/Untertitel-/Video-QC nachweisen.
4. Separates TikTok-Konto für Jori & Flimm verbinden, private/draft Veröffentlichung testen; keinerlei Vermischung mit \`motus614\`.
5. GitHub-Standardzweig und Schedule erst nach abgeschlossener Testkette und expliziter Freigabe aktivieren. Folge am Vorabend erstellen, um **14:00 Uhr** für den kommenden Tag einplanen und den tatsächlichen Sendestatus prüfen.

## Kostenregel und Sicherheit
- Github Actions Standard-Runner im **öffentlichen** Repository sind laut GitHub grundsätzlich kostenlos. Artefaktspeicher sowie externe Dienste und Kontokontingente separat prüfen.
- Keine automatische kostenpflichtige Verpflichtung, kein Blind-Retry bei Text-/Bild-/Voice-Problemen, kein Upload von privaten Buchdateien an den öffentlichen Dienst.
- Das Bezahlinhalt-Grenzprotokoll gilt: 24 Buchmissionen/48 Buchaufgaben und Lösungen bleiben im Buch, freie Videofolgen müssen neu sein.
- Bei gescheitertem Teilprozess ist die Folge **nicht veröffentlicht**, auch wenn Skript oder Renderer gestartet wurde.
- Nach jeder neuen Version: Datei, Umsetzung, Testnachweis, offene Fehler und nächsten Schritt dokumentieren.
