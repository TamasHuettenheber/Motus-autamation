# Jori & Flimm – Produktionsstand 23.10.2026 (Folge 006, korrigierte Vorschau)

Stand: 23.10.2026 20:05 Europe/Berlin. Branch: `feature/jori-flimm-neustart-folge001`.

## Folge 006 – „Der Ton im Glashaus“

- Die Handlung setzt direkt am riesigen Fußabdruck und Sterngeheimnis aus Folge 005 an. Jori ist durchgehend ein Mädchen. Das Klangrätsel wird mit der langen Glasröhre gelöst; danach folgen Sternkarte, Teleskop und eine neue Gestalt als Cliffhanger.
- Fünf eigenständige, neu erzeugte Szenenbilder mit folgenspezifischen Hintergründen.
- Nach Tamás' Sichtprüfung wurde die Rätselkarte aus dem Lösungsbild entfernt. Sie bleibt während der Rätsel-Pause sichtbar und verdeckt die anschließende Auflösung nicht mehr.
- Renderlogik aktualisiert in Commit [740a517](https://github.com/TamasHuettenheber/Motus-autamation/commit/740a517c011907612598a8ad838ce7068985095a); der isolierte Vorschau-Workflow reagiert nun auch auf Änderungen an dieser Renderlogik.
- Tatsächlicher GitHub-Renderlauf [39999834452](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39999834452) ist erfolgreich abgeschlossen. Action-Logs bestätigen Story-/Bild-QC, Sulafat-TTS, fertige MP4 und MP4-QC.
- Aktualisierte Vorschau: [Folge 006 ansehen / herunterladen](https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-27-e006.mp4).
- Action-Metadaten: H.264/AAC, 720×1280 (9:16), 131,76 s, 6.267.763 Bytes. Die Sprachdatei enthält eine stille Pause von exakt 7,000 s; geringe AAC-Codec-Abweichung in der fertigen MP4 ist akzeptabel.

## Noch offene Veröffentlichungskontrollen

- Die Untertitel werden derzeit proportional aus Textlängen verteilt. Eine präzise Satz-/Wortausrichtung am fertigen Sulafat-Audio ist noch offen.
- Kein physischer iPhone-Abspieltest wurde durchgeführt.
- Buffer wurde nicht verändert und Folge 006 wurde nicht eingeplant. Vor einer späteren Buchung muss die Queue live erneut geprüft werden.

## Kosten / Produktionsweg

- Sulafat wurde mit dem bestehenden Modell `gemini-3.8-flash-lite-tts` erzeugt. Der bestätigte Standard-Free-Tier-Zugang blieb unverändert; kein Paid-/Batch-/Flex-/Priority-Modus und keine neue Kostenverpflichtung.
- Es wurden keine MOTUS-Dateien oder -Workflows geändert.
