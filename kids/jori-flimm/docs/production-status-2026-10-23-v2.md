# Jori & Flimm – Produktionsstand 23.10.2026 (Nachtrag)

Stand der tatsächlichen Prüfungen: **23.10.2026, 17:24 Europe/Berlin**. Branch: `feature/jori-flimm-neustart-folge001`; HEAD `91810074dcdfd8addad52517c0f694d54b373238`.

## Folge 006 – „Der Ton im Glashaus“

- Storyentwurf: [episode_006_story_draft.json](../relaunch-v2/episode_006_story_draft.json). Die Handlung setzt unmittelbar beim Fußabdruck und Sterngeheimnis von Folge 005 an. Das Rätsel vergleicht drei verschieden klingende Glasröhren. Frage und Klanghinweise stehen vor der Lösung; der Entwurf enthält genau einen Marker `[[PAUSE:7]]`. Jori wird weiblich referenziert.
- Fünf neue, unterschiedliche Szenenbilder liegen in [assets/episode-006](../relaunch-v2/assets/episode-006/). Die vorherige Sichtprüfung bestätigte eigene Motive und folgenspezifische Hintergründe; Maße 941×1672 px, nahe 9:16.
- Jori-only Produktionshelfer wurden in Commit [e58c67f](https://github.com/TamasHuettenheber/Motus-autamation/commit/e58c67f97128327c07c55f8c2782883440dc14eb) für Folge 006 erweitert: Voice-Wrapper liest den neuen Entwurf; Renderer nutzt die fünf PNGs und zeigt während der Rätselpause Zielklang und alle drei Optionen; Buffer-Helfer kann Folgenummer, Datum und Titel für Folge 006 verarbeiten.
- GitHub-Qualitätslauf [39977747110](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39977747110) ist **erfolgreich**: Python-Compile, Story-/Kontinuitätstests, Vorschau-Dry-Run für E006 am 27.10. und bestehende Relaunch-Tests. Der Lauf hat **kein TTS, keinen Render und keine Buffer-Buchung** ausgeführt.
- **Noch keine fertige Folge-006-MP4.** Bild-/Sprechsynchronität, echte Sulafat-Aufnahme, Untertitel-Timing, Videospuren/-dauer und tatsächlich gemessene sieben Sekunden Stille sind daher noch nicht final prüfbar. Kein Buffer-Post für Folge 006.

## Google-Tarif und Kosten

- Der vom Nutzer übermittelte AI-Studio-Screenshot zeigt das angemeldete Google-Konto unten links. Das belegt die Anmeldung in der ChatGPT-iPhone-Browseransicht.
- Der Screenshot zeigt **nicht** den ausgewählten Google-Cloud-Projektnamen oder dessen **Billing Tier**. Ein anderer, für mich erreichbarer Chrome-Kontext ist getrennt davon und war abgemeldet. Die vorherige Gleichsetzung dieser beiden Browser-Sitzungen war falsch.
- Der Tarif des konkreten Projekts bleibt damit unbestätigt. Entsprechend wurde in diesem Lauf kein Google-TTS-Aufruf ausgelöst; es wurde kein Tarifwechsel und keine Kostenverpflichtung vorgenommen.

## Tatsächlicher Buffer-/TikTok-Stand (nur lesend verifiziert)

Read-only Action [39977943484](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39977943484), 23.10.2026 17:24 Europe/Berlin: richtiger Kanal **@jori.flimm**; keine MOTUS-Aktion. Der Lauf meldete: keine Posts erstellt, geändert oder veröffentlicht.

| Folge | Tatsächlicher Buffer-Status | Buffer-ID | Tatsächlicher Termin / Link |
|---:|---|---|---|
| 001 | sent | `6ad9ce4baefa17e341f96c3f` | 22.10., 14:00 CEST; [TikTok](https://tiktok.com/@jori.flimm/video/7699461062835309857) |
| 002 | sent | `6ad9d2f9a013397d9328faea` | 23.10., 14:00 CEST; [TikTok](https://tiktok.com/@jori.flimm/video/7699832623979449632) |
| 003 | scheduled | `6ad9d321a013397d932908dc` | 24.10., 14:00 CEST |
| 004 | scheduled | `6ad9d34aaefa17e341fad444` | 25.10., 14:00 CET |
| 005 | scheduled | `6ad9d373e6aee73a2b15d107` | 26.10., 14:00 CET |
| 006 | nicht vorhanden | — | Nächster freier täglicher Slot: **27.10.2026, 14:00 CET** (Buffer-UTC: `2026-10-27T13:00:00Z`) |

Vor einer späteren Buchung von Folge 006 muss die aktuelle Queue erneut geprüft werden. Bestehende korrekte Buchungen 003–005 wurden nicht geändert.

## Nächster Schritt

Für Folge 006 den Projekttarif in AI Studio unter **Projects → Billing Tier** nachweisen. Nur wenn das konkrete Projekt im Free Tier steht, den TTS-Schritt starten. Danach MP4 rendern, echte MP4-/Audio-/Untertitel-/Pausen-QC durchführen und erst dann Folge 006 auf @jori.flimm für den freien Termin buchen. MOTUS-Dateien und -Workflows bleiben unangetastet.
