# Jori & Flimm – Produktionsstand 23.10.2026 (Folge 006 Preview)

Stand: 23.10.2026 17:48 Europe/Berlin. Branch: `feature/jori-flimm-neustart-folge001`.

## Billing / Google TTS

- Die bestehende Projektentscheidung wurde wieder aufgenommen: `gemini-3.8-flash-lite-tts`, Standard-Free-Tier-Ausführung, bestehender GitHub-Key `JORI_GEMINI_API_KEY`.
- Folge 006 wurde mit Sulafat erfolgreich vertont. Es gab keinen Tarifwechsel, keine Paid-, Batch-, Flex- oder Priority-Ausführung und keinen neuen Abrechnungs-/Kostenvertrag.

## Folge 006 – „Der Ton im Glashaus“

- Storyentwurf: [episode_006_story_draft.json](../relaunch-v2/episode_006_story_draft.json). Setzt direkt beim riesigen Fußabdruck und dem Sterngeheimnis aus Folge 005 an. Jori durchgehend weiblich; Rätsel: Welche Röhre wiederholt den tiefen Doppelton? Antwort: die lange Röhre. Danach Sternkarte, Teleskop und neue Gestalt mit zweitem Stern als Cliffhanger.
- Fünf neue Szenenbilder: jeweils 941×1672 px, fünf unterschiedliche Dateien/Hashes. In der Sichtprüfung zeigen sie den Fußabdruck, das Glashaus, die drei Röhren, die Lösung und den neuen Cliffhanger.
- Tatsächlicher GitHub-Produktionslauf [39981039332](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39981039332) erfolgreich. Story-/Bild-QC, Sulafat-TTS, Render und Upload wurden tatsächlich ausgeführt. Es wurde **kein Buffer-Post** angelegt.
- MP4: [Folge 006 – GitHub-Datei](https://github.com/TamasHuettenheber/Motus-autamation/blob/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-27-e006.mp4) · [Raw-MP4](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-27-e006.mp4)
- Tatsächliche MP4-Metadaten aus Action-Log/ffprobe: H.264, AAC, 720×1280 (9:16), 130,68 s, 6.039.194 Bytes. TTS-Log: Sulafat, 130,68 s.
- Sichtprüfung der MP4-Stichproben bestätigte fünf eigenständige Szenenhintergründe. Während der Rätselszene sind Frage, Zielklang und alle drei Hinweise sichtbar.

## QC-Befund – noch keine Veröffentlichungsfreigabe

- Die stille Tondatei enthält einen 7,000-s-Pausenabschnitt. Eine nachgelagerte Messung der **fertigen AAC-MP4** mit ffmpeg `silencedetect=noise=-60dB:d=6.5` ergab jedoch Stille von 73,7193 bis 80,8119 s, also **7,09254 s**. Damit ist „genau sieben Sekunden“ in der fertigen Datei noch nicht nachgewiesen; die Folge bleibt Preview.
- Die Untertitelzeiten des aktuellen Renderers werden proportional aus Textlängen geschätzt. Das Regelwerk erklärt diese Heuristik ausdrücklich als nicht veröffentlichungsreif. Eine echte Wort-/Satz-Ausrichtung am fertigen Sulafat-Audio fehlt noch.
- Kein physischer iPhone-Abspieltest durchgeführt. Lautheitsmessung allein ersetzt diesen Test nicht.

## Buffer / Veröffentlichung

- Die letzte tatsächliche, schreibgeschützte Queue-Prüfung [39977943484](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39977943484) bestätigte @jori.flimm und Folge 006 als nicht vorhanden; Folgen 001–005 blieben unangetastet.
- Folge 006 ist weiterhin **nicht geplant**. Vorgesehener nächster Slot: **27.10.2026, 14:00 Europe/Berlin**. Vor einer Buchung die Buffer-Queue erneut live prüfen. Veröffentlichung erst nach Korrektur der Pause, belastbarer Untertitel-Synchronisierung und vollständigem MP4-QC.

## Nächster Produktionsschritt

TTS-Randstille vor und nach der markierten Pause trimmen, sodass die Frage bis zum tatsächlichen Sprechende sichtbar bleibt und die anschließende Stille in der kodierten MP4 exakt sieben Sekunden beträgt. Danach die Untertitel direkt am gerenderten Audio ausrichten und die komplette MP4 erneut prüfen. MOTUS-Workflows und -Dateien wurden nicht geändert.
