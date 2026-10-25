# Jori & Flimm – technische Übergabe V2, 21. Oktober 2026

## Ergebnis
**Prototyp mit realem vollständigem GitHub-Videorender bestanden, jedoch kein autonomer öffentlicher Tagesbetrieb.** Die regulären MOTUS-Abläufe wurden nicht verändert. Alles liegt auf `feature/jori-flimm-kids-pipeline` (PR #66), nicht auf `main`.

## Neue/erweiterte Dateien
- `scripts/generate_daily_story.py`: geordnete Serienfortsetzung bis maximal sieben unveröffentlichte Entwürfe; vorhandene unfreigegebene Test-Episoden reservieren ihre Nummern; prüft Datums-/Nummern-/Rätselduplikate und Sprechnarration einschließlich sieben Sekunden Denkpause. Externer Gemini-API-Zugang fehlt; noch **keine tägliche neue KI-Folge nachgewiesen**.
- `scripts/build_storyboard.py`: erstellt aus sechs Szenenbriefs sechs 720x1280-JPG-Montagen bestehender, eigener Jori-&-Flimm-Illustrationen. Achtung: keine neuen KI-Illustrationen und **keine motivgenaue Szenenanpassung**. Manuskript und Manifest markieren den Inhalt ausdrücklich als nicht freigegeben.
- `scripts/compile_preview_episode.py`: bereitet aus den sechs Montagen einen `preview_only: true`-Renderer-Auftrag für 14:00 Uhr vor, mit drei unbestätigten QC-Gates; kein Publisher.
- `scripts/test_generate_daily_story.py`, `test_build_storyboard.py` und `test_compile_preview_episode.py`: insgesamt **12 Tests bestanden**.
- `.github/workflows/jori-flimm-daily-draft.yml`: offline getestet, Vorgang `39662826423`. Wenn irgendwann aktiviert, soll sie Folge für den Folgetag abends 22:17 Uhr Europe/Berlin vorbereiten, sechs Bildmontagen erzeugen, dann einen privaten Video-Preview-Auftrag auf demselben separaten Entwicklungszweig bereitstellen. Bis zum Merge in `main` und Aktivierung der GitHub-Variable `JORI_STORY_DRAFTS_ENABLED` entsteht kein Echtbetrieb; kein unabsichtlicher API-Aufruf.
- `.github/workflows/kids-render.yml` und `episode-state.schema.json`: streng getrennter `preview_only`-Modus; er erstellt Videoartefakte ohne veröffentlichte Beiträge und ohne Fortschreiben der verbindlichen Serien-/Episodenstanddateien.
- `fixtures/e002-draft-2026-10-22.json` und `episodes/jori-flimm-2026-10-22-e002.json`: eigenständige Episode 002 „Die Glocke hinter dem Brückentor“, **nur Testfassung**.

## Realer End-to-End-Test
- GitHub Actions Run [39662312812](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39662312812), **success**.
- Episode 002, 78,208 Sekunden, 1080×1920, H.264-Video + AAC-Audio 48 kHz; fertiges MP4-Artefakt unter `jori-flimm-2026-10-22-e002` (7 Tage Archivfrist, erstellt 21. Oktober).
- Gratisstimme Victoria wurde diesmal tatsächlich generiert; Spracherzeugung, Untertitel, bewegte Szene, MP4-Mux und technische QC liefen erfolgreich.
- Ein erster Renderanlauf Run `39662143987` scheiterte wegen fehlender verpflichtender Victoria-Stimmenkonfiguration im Storypayload; Eingabe korrigiert; zweiter Run erfolgreich.
- Video visuell als Stichprobenübersicht geprüft: stabiles, ansprechendes Jori-&-Flimm-Design und gut sichtbare Untertitel. **Inhaltliche Visual-QC nicht bestanden**, denn der erzählte Igel und drei Glocken erscheinen nicht motivgerecht; die alten Motive zeigen hauptsächlich die beiden bekannten Figuren und das Brückentor. Daher nicht öffentlich verwenden.
- Ein direkter MP4-Abzug wurde lokal erstellt und in der persönlichen Bibliothek unter `/Jori & Flimm/Testfolgen/Jori_Flimm_Folge_002_Vorschau.mp4` gespeichert. Keine TikTok-Übertragung oder Veröffentlichung.

## Technische Grenzen und Pflichten vor Freischaltung
1. **Neue Originalillustrationen passend zu jeder Folge** sind noch nicht kostenlos und zuverlässig automatisiert. Der vorhandene Montageweg ist nur ein Fallback für interne Layout-, Timing- und Ton-Tests.
2. Die echte nächtliche neue KI-Story benötigt einen separaten gültigen Free-Tier-API-Schlüssel als GitHub Secret `JORI_GEMINI_API_KEY`. Rate/Billing der konkreten Kontokonfiguration sind nicht geprüft. Keine kostenpflichtigen Dienste auslösen.
3. GitHub-Actions-Schedules laufen nur vom **Default-Branch**; Entwurfsworkflow ist bewusst ausschließlich im Feature-Branch. GitHub-Scheduler-Ausführung kann sich zudem verzögern. Der 14-Uhr-Zeitpunkt sollte als Publisher-geplante Zeit behandelt werden, nicht als garantierter Cron-Push.
4. Separater TikTok-Account „Jori & Flimm“ muss vom Nutzer angelegt/autorisiert und auf einen geeigneten kostenlosen Publisher verbunden werden. Der einzige derzeit verbundene Metricool-TikTok-Kanal ist MOTUS; diesen nicht verwenden.
5. Wer eine tatsächliche Veröffentlichung behauptet, muss `sent` plus TikTok-Link prüfen. Ohne diese beiden Fakten nur `scheduled/pending` melden.
6. Buchmissionen, Rätsel und Lösungen sind bezahlten Büchern vorbehalten; die Serienfolge muss neu bleiben. Vor Livebetrieb echte visuelle/inhaltliche Qualitätskontrollen statt bloßer Bool-Gates einführen.

## Nächste sinnvolle Phase
- Für mindestens eine Episode sechs motivpassende neue Bilder erzeugen; Realvideo erneut rendern, hören und visuell prüfen.
- Dann sieben unabhängige Tagesläufe mit Story- und Bildproduktion als **interne Testserie** nachweisen.
- Separaten Jori-&-Flimm-TikTok-Kanal authorisieren und zunächst einen privaten Publisher-Test durchführen.
- Erst danach GitHub-Schedule auf `main` freigeben und eine überprüfte 14-Uhr-Publishing-Kette einschalten.

## Kostenstatus
Keine kostenpflichtigen Verpflichtungen abgeschlossen. 0 € nachweisbare zusätzliche Ausgaben in dieser GitHub-Teststrecke; unabhängige Kontingente/Preise externer Bild- oder Textgeneratoren nicht implizit freigegeben.
