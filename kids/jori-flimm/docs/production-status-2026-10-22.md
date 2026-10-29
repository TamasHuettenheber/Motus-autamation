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

Der Zeitplan ist derzeit **noch nicht aktiv**: GitHub führt `schedule`-Workflows nur aus, wenn die Workflow-Datei im Standard-Branch liegt; außerdem verlangt der Job die Repository-Variable `JORI_RELAUNCH_AUTO_DRAFTS=true`. Der aktuelle Arbeitszweig bleibt `feature/jori-flimm-neustart-folge001`. Eine Aktivierung wurde nicht vorgenommen, damit weder der Standard-Branch/MOTUS berührt noch ein laufender Gemini-API-Aufruf ohne bestätigte Kostenfreigabe ausgelöst wird. Eine manuelle `workflow_dispatch`-Auslösung ist im YAML vorbereitet, aber erst verfügbar, wenn die Workflow-Datei im Standard-Branch liegt.

MOTUS-Workflows und Metricool wurden nicht geändert bzw. verwendet.


## Aktualisierung 27.10.2026 – Folge 008 korrigierte Rätselszene

- Folge 008 „Die Hüterin des dritten Sterns“ setzt direkt am dritten goldenen Stern und dem Schatten unter dem Eis aus Folge 007 an. Das Rätselbild wurde korrigiert: drei Tiere bleiben sichtbar; die Hinweise stehen knapp als Glocke/Tentakel, ein Silberfleck und kein Panzer. Der Rätseltext führt anschließend ausdrücklich zur Mondqualle.
- Story-/Bildprüfung: sechs unterschiedliche, neue 9:16-Szenenbilder; Storykontinuität, weibliche Jori-Pronomen und rätselspezifische Hinweise bestanden. Die isolierte Qualitätsprüfung bestand nach Korrektur ihrer Groß-/Kleinschreibungsannahme in Run [40428254818](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40428254818).
- Fertige MP4: [Folge 008 v2](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-29-e008-v2.mp4). Der erfolgreiche Wiederanlauf ist Run [40245336647, Versuch 2](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40245336647). Dauer 134,208 s; H.264 720×1280 plus AAC; Untertitel-Tokenprüfung bestanden; gemessene echte Stille 7,040 s. Die fertige MP4 wurde zusätzlich visuell stichprobengeprüft: Rätselbild während der Pause, Auflösung ab 87,28 s, anschließende Sternwartenhandlung und neuer Cliffhanger.
- Buffer-Eintrag wurde **in place** aktualisiert, ohne Duplikat oder Terminänderung: Run [40428195810](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40428195810) bestätigt Post-ID `6ade8a490b5343d070f6b831`, Status `scheduled`, Kanal `@jori.flimm` / `6ad948ea778b240e2f839607`, dueAt `2026-10-29T13:00:00Z` = **29.10.2026, 14:00 Europe/Berlin**. Buffer-Antwort nennt als Asset-Quelle die v2-MP4. Die Buffer-Oberfläche bestätigte am 27.10. denselben geplanten Termin. Kein Veröffentlichungsnachweis für Folge 008; sie ist geplant, nicht veröffentlicht.
- Kosten-/Kontingentwissen für die folgenden Läufe: Sulafat verwendet `gemini-3.8-flash-lite-tts` im **kostenlosen Free Tier**. Die tatsächliche API-Fehlermeldung vom 25.10. nannte ein Limit von **10 Anfragen pro Tag** und eine Wartezeit bis zum Reset; ein späterer Wiederanlauf am 27.10. erzeugte Sulafat erfolgreich. Bei 429 bis zum Reset warten; weder Paid-Tier noch Batch/Flex/Priority oder Abrechnungswechsel aktivieren und keine Ersatzstimme verwenden.
- Folge 008 bleibt auf dem bereits freigegebenen 14:00-Slot. Es wurde keine zweite Buchung erzeugt; die frühere v1-Mediendatei wurde durch v2 ersetzt.


## Aktualisierung 27.10.2026 – Folge 009 in Arbeit

- Story: „Das Sternbild ohne Anfang“ setzt direkt beim Glockenschlag und der rotierenden Unterwassersternwarte aus Folge 008 ein. Das neue visuelle Rätsel hat drei Sternenwege; nur die mittlere Linie schließt sich. Jori ist durchgehend weiblich beschrieben. Der Cliffhanger zeigt ein lichtähnliches Doppel von Flimm.
- Bildprüfung: sechs neue, eigenständige Szenenbilder im 9:16-Format wurden im isolierten Jori-Branch abgelegt. Beim ersten Sichtcheck wurde die Rätselszene ersetzt, weil mehrere Pfade geschlossen wirkten; die neue Szene zeigt nur einen geschlossenen Kreis. Story-, Python-Syntax-, Pronomen- und sechs Bilder umfassende Einzigartigkeitsprüfung bestanden.
- GitHub-Preview [Run 40430531607](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40430531607) erreichte Sulafat-TTS im Free Tier; der Lauf scheiterte danach an falsch zusammengefassten Segmentmarkern. Die Marker wurden korrigiert.
- [Run 40430737091](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40430737091) bestätigt erneut Story-/Bild-QC, stoppte aber sicher vor dem Render bei Google HTTP 429: Free-Tier-Limit **10 Anfragen pro Tag**, nächste Anfrage laut API nach 5 h 50 min 55 s (ca. 08:00 Europe/Berlin). Keine kostenpflichtige Stufe, kein Tarifwechsel und keine Ersatzstimme verwendet. Nach Reset E009-TTS fortsetzen, dann MP4 vollständig rendern und prüfen.
- Folge 009 ist noch nicht fertig, nicht veröffentlicht und nicht in Buffer eingeplant. Der nächste geplante Lauf der bestehenden Jori-Automation ist auf 27.10.2026, 08:10 Europe/Berlin gestellt, damit der Reset abgewartet wird und der freie 30.10.-Slot mit mindestens drei Tagen Vorlauf erreichbar bleibt.


## Abschluss 27.10.2026 – Folge 009 „Das Sternbild ohne Anfang“

- Kontinuität und Story: Folge 009 setzt direkt bei Glockenschlag und rotierender Unterwassersternwarte aus Folge 008 ein. Jori ist durchgehend weiblich; Flimm bleibt als kleines goldenes Wesen mit grüner Mütze und leuchtendem Bauchstern konsistent. Das neue Rätsel zeigt drei Sternenwege; ausschließlich der mittlere Weg schließt sich.
- Bilder: sechs neue, unterschiedliche 9:16-Szenenbilder mit folgenspezifischen Unterwasser-Sternwarten-Hintergründen. Das erste Rätselbild wurde verworfen, weil mehrere Linien geschlossen wirkten; die ersetzte Version ist eindeutig. Bild- und Story-QC bestanden.
- Sulafat und Render: Der erfolgreiche Free-Tier-TTS- und Preview-Lauf ist [40430737091](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40430737091), Versuch 2. Die tatsächliche MP4 wurde anschließend visuell bei 2, 10, 16, 30, 42, 48,5, 54,5, 55,5, 65, 79, 88 und 93 Sekunden geprüft. Dabei wurde ein zu lange sichtbarer Lösungsbalken entdeckt und in v2 entfernt. Die unabhängige Endprüfung [40467317964](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40467317964) bestätigt: 94,125 s, H.264 720×1280, AAC Sulafat, sechs neue Bilder, 7,05325 s echte Stille und kein verbleibender Lösungsbalken. Untertitel liegen außerhalb der Stille und folgen den fünf tatsächlichen Sprechsegmenten.
- Fertige MP4: [Folge 009 v2](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-30-e009-v2.mp4).
- Live-Buffer-Prüfung [40465902310](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40465902310) bestätigte vor Buchung drei vorhandene geplante Posts für Folgen 006–008 und den freien 30.10.-Slot. Der Release-Lauf [40467527989](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40467527989) bestätigt die tatsächliche Buffer-Antwort: Post-ID `6ae05359da2ca338b1513bea`, Status `scheduled`, Kanal-ID `6ad948ea778b240e2f839607` / `@jori.flimm`, dueAt `2026-10-30T13:00:00.000Z` = **30.10.2026, 14:00 Europe/Berlin**. Asset-Quelle ist die v2-MP4. Kein Veröffentlichungsnachweis; Folge 009 ist geplant, nicht veröffentlicht.
- Kosten-/Limitnachweis: Sulafat wurde mit `gemini-3.8-flash-lite-tts` im Free Tier erzeugt. Ein zusätzlicher, für die Endkorrektur nicht benötigter Preview-Trigger stoppte bei der separaten Free-Tier-Minutenbegrenzung von drei Anfragen pro Minute; die bereits erzeugte Sulafat-Aufnahme wurde kostenfrei weiterverwendet. Keine kostenpflichtige Stufe und keine Ersatzstimme.


## Aktualisierung 28.10.2026 – Folge 010 „Das rückwärts leuchtende Echo“

- Die Story setzt unmittelbar beim rückwärts leuchtenden Flimm-Licht aus Folge 009 an. Das neue Rätsel führt aus der erlöschenden Reihenfolge Blau–Silbern–Gold zur goldenen Kugel; danach öffnet sich die Tür und ein tiefblauer Lichtpunkt unter der Sternwarte bildet den neuen Cliffhanger.
- Sechs eigenständige, eigens für Folge 010 erzeugte Hintergründe liegen im Jori-Branch. Story- und Bildprüfung bestätigen sechs unterschiedliche 9:16-Szenen, Joris weibliche Pronomen und Flimms sichtbare Nase, grüne Mütze und Bauchstern. Der Szenenwechsel zu den Glaskugeln wurde an Joris Entdeckung herangerückt.
- Fertige GitHub-MP4: [Folge 010 v2](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-31-e010-v2.mp4). Der [Preview-Renderlauf 40651535840](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40651535840) und die unabhängige [Final-QC 40651869403](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40651869403) bestanden. Die tatsächliche MP4 ist 144,325 s, H.264 720×1280 mit AAC-Sulafat; Untertitel-Tokenprüfung bestanden, gemessene stille Rätselpause 7,0116 s. Stichproben im fertigen Video prüfen Szenenwechsel, Bild/Text-Bezug, Rätselkarte, Auflösung und Cliffhanger.
- Der [Live-Buffer-Check 40651869130](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40651869130) bestätigte vor der Buchung @jori.flimm / Kanal-ID `6ad948ea778b240e2f839607`, die bestehenden geplanten Folgen 007–009 für 28.–30.10. und den freien 31.10.-Slot. Der [Release-Lauf 40652037112](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40652037112) erhielt die tatsächliche Buffer-Antwort: Post-ID `6ae1a823f94c111d6ec185a7`, Status `scheduled`, Kanal-ID `6ad948ea778b240e2f839607`, dueAt `2026-10-31T13:00:00.000Z` = **31.10.2026, 14:00 Europe/Berlin**. Die Asset-Quelle in der Antwort ist die obige v2-MP4.
- Folge 010 ist **eingeplant, nicht veröffentlicht**; es liegt noch kein Buffer-/TikTok-Nachweis `sent` mit externer TikTok-URL vor. Der Free-Tier-TTS-Lauf verwendete fünf Anfragen im Abstand von 22 Sekunden; der korrigierte Renderlauf verwendete dieselbe Sulafat-Aufnahme erneut und löste keine weiteren TTS-Anfragen oder Kosten aus.


- Der Read-only-Nachcheck nach der Buffer-Änderung [40652354211](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40652354211) bestätigt vier geplante Beiträge und genau einen Folge-010-Post mit ID `6ae1a823f94c111d6ec185a7`, `scheduled`, dueAt `2026-10-31T13:00:00.000Z`. Der idempotente Release-Nachlauf [40652354155](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40652354155) fand dieselbe vorhandene Buchung und erzeugte keinen Duplikatpost. Die zusätzliche Jori-Qualitätsprüfung [40652354229](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40652354229) war ebenfalls erfolgreich.


## Folge 011 — Der Sternstein im blauen Saal

- **Story:** direkte Fortsetzung von Folge 010 an der bebenden Treppe und dem tiefblauen Licht. Neues visuelles Formrätsel; danach beruhigt der Sternstein die Treppe und die Karte unter dem Glassaal führt zum nächsten Cliffhanger.
- **Bilder und Kontinuität:** acht eigens für Folge 011 erzeugte, unterschiedliche 9:16-Szenenbilder (720×1280). Nach der Sichtprüfung wurden zwei neue Übergangsbilder ergänzt: Treppe bis zur gesprochenen Glassaal-Enthüllung sowie sinkendes Mosaik bis zur gesprochenen Kartenenthüllung. Jori bleibt weiblich; Flimms runde Nase, grüne Mütze, roter Bommel und Bauchstern sind konsistent.
- **Render-QC:** 126,520 s, 720×1280 H.264/AAC, Sulafat; acht neue Bilder; Untertitel-Tokenprüfung bestanden. Source-Pause exakt 7,000 s; MP4-Silence-Detection 7,011833 s. Rätsel-Frage und Bildhinweise bleiben während der Pause sichtbar. Die Satz- und Bildwechsel wurden an der tatsächlichen Szenenenthüllung geprüft.
- **MP4:** [Folge 011 ansehen](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-11-01-e011-v1.mp4).
- **GitHub-Nachweise:** [Preview/Render](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40838905570), [unabhängiger Final-QC](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40839383801), [Buffer-Liveprüfung vor Buchung](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40839421490), [Release](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40839634275), [Buffer-Nachcheck](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40839817576).
- **Buffer:** Status scheduled, Post-ID 6ae2fe729c83386213567a72, Kanal @jori.flimm (6ad948ea778b240e2f839607), dueAt 2026-11-01T13:00:00.000Z = **01.11.2026, 14:00 Europe/Berlin**. Der Nachcheck fand denselben einzelnen Beitrag; er ist geplant, nicht bereits veröffentlicht.
- **Kosten:** sechs Sulafat-Anfragen im verifizierten Free Tier; die Renderkorrektur verwendete den gespeicherten Ton und löste keine weitere TTS-Anfrage aus. Keine kostenpflichtige API und kein Upgrade.


## TikTok-Safe-Zone-Korrektur Folgen 010 und 011

- Nutzerfeedback vom 29.10.2026: Rätselschilder und lösungsrelevante Hinweise dürfen nicht unter den rechten TikTok-Bedienelementen liegen. Das veröffentlichte Ausgangsvideo bleibt unverändert; für alle künftigen Folgen ist die Safe-Zone verbindlicher QC-Blocker.
- Folge 010 und 011 wurden vor ihrer Veröffentlichung korrigiert. Frage und sämtliche Antwortmöglichkeiten liegen nun bei 720×1280 vollständig links von x=540; der Bereich ab x=560 bleibt für Herz, Kommentare, Teilen und Profil frei.
- Der [Korrektur- und Buffer-Lauf 40847854026](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/40847854026) bestand. MP4-Technik und Ton blieben unverändert: Folge 010 144,325 s mit 7,011625 s Stille; Folge 011 126,520 s mit 7,011833 s Stille.
- Buffer ersetzte nur die Medien der vorhandenen Posts: Folge 010 behielt Post-ID `6ae1a823f94c111d6ec185a7` und den 31.10.2026, 14:00 Europe/Berlin; Folge 011 behielt Post-ID `6ae2fe729c83386213567a72` und den 01.11.2026, 14:00 Europe/Berlin. Status jeweils `scheduled`, Kanal `@jori.flimm`; keine neuen oder doppelten Posts.
