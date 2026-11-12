# Jori & Flimm – Sprecherinnen-Casting und Handy-Audio-QA, 21.10.2026

## Anlass und Nutzerfeedback
- Alte Victoria-Stimme: österreichischer Akzent wird abgelehnt.
- Piper-Kerstin: klingt zu stark nach standardisiertem Hochdeutsch, trocken/lehrerhaft; ebenfalls abgelehnt.
- Gesucht wird eine natürliche, ältere, warmherzige Frauenstimme, wie eine **Omi beim Vorlesen**, mit lebendiger, liebenswerter Betonung.
- Nutzer hört bestehende MP4 trotz voll aufgedrehter iPhone-Lautstärke kaum. Audio auch technisch prüfen und gegen MP3 im unabhängigen Player testen; **nicht** allein LUFS als Beweis tatsächlicher Hörbarkeit interpretieren.

## Technisch verifiziert
- Bisherige MP4 V2 gemessen: -16.51 LUFS, etwa -1.33 dBTP. Datei nicht stumm; iOS-Player-/Audio-Routing-Problem bleibt möglich.
- Gemini 3.8 Flash TTS hat laut offizieller Gemini Developer API Pricing-Seite einen Free Tier; bestehender API-Key wurde für drei kurze Hörproben verwendet, ohne Paid-Upgrade.
- Drei unabhängige 24–25-Sekunden-MP3-Hörproben in einem erfolgreichen GitHub-Workflow erstellt:
  [GitHub Actions Run 39683836307](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39683836307)
  - **Gacrux**: weiblich/reif, -13.97 LUFS, -0.95 dBTP
  - **Vindemiatrix**: weiblich/sanft, -14.53 LUFS, -0.98 dBTP
  - **Sulafat**: weiblich/warm, -13.98 LUFS, -1.18 dBTP
- Artefakt `Jori-Flimm-Omi-Erzaehlstimmen-LAUT-PROBEN` enthält WAV und MP3, sieben Tage Downloadfenster. MP3-Dateien wurden auch nach `/mnt/data/jori_omi_stimmproben/` entpackt und dort geprüft.
- Zusätzlich lokal eine **24,68 Sekunden lange MP4** erstellt, die denselben Gacrux-MP3-Sprechertext und das gleiche Audiosignal wie der MP3-Test verwendet. Das erlaubt einen Handy-Abspielvergleich MP3 vs MP4, bevor behauptet wird, die Produktionsdatei sei schuld. MP4: `/mnt/data/Jori_Flimm_Omi_Gacrux_Vergleich_MP4.mp4`.

## Änderungen im getrennten Entwicklungszweig
- `scripts/voice_audition_gemini.py` erstellt drei kurze Audio-Only-Hörproben mit Gemini 3.8 Flash TTS über den vorhandenen GitHub Actions Secret `JORI_GEMINI_API_KEY`. Die Abspielproben sind mono MP3 und enthalten einen Sprachverständlichkeit-Equalizer, Dynamikbearbeitung und Loudness-Normalisierung. Keine Social-Veröffentlichung.
- `scripts/generate_voice_gemini.py`: optionaler TTS-Provider mit genau `Gacrux`, `Vindemiatrix`, `Sulafat` als zulässigen Stimmen; verarbeitet die explizite 7-s-Rätsel-Denkpause und schreibt `work/narration_source.wav` mit `work/voice-timeline.json`.
- `episode-state.schema.json`: weitere optionale TTS-Auswahl; keine bisherige Episode wurde automatisch darauf umgestellt.
- `.github/workflows/kids-render.yml`: im Feature-Branch vorbereiteter Auswahlzweig für Gemini 3.8 TTS, stärkeres Sprach-EQ/Dynamik-Processing und deutlich strengerer Mobile-Audio-QC-Gate. Der Test einer vollständigen neu gesprochenen Episode steht aus.
- `.github/workflows/jori-flimm-daily-draft.yml`: Syntaxprüfung der neuen TTS-Python-Datei im isolierten Offline-CI.

## Offene Entscheidungen / Qualitätsprobleme
1. Nutzer wählt bevorzugte Stimme nach tatsächlichem Hören; nicht automatisch die harte Kerstin-/Victoria-Stimme reaktivieren.
2. Überprüfung MP3/MP4 des **identischen Audios** auf dem iPhone. Wenn MP3 laut, MP4 leise: Quick Look/ChatGPT Video-Player oder Audio-Routing auf dem Gerät prüfen. Wenn beide leise: Lautsprecher, Bluetooth-/AirPlay-Ausgang und sonstige Geräte-Audioeinstellungen prüfen.
3. Neue Stimme in Episode 002 über den GitHub-Renderer vertonen und synchronisiert rendern, bei Prüffehlern nicht veröffentlichen.
4. Für bezahlbar/nutzbar tägliche Serie weiterhin passende Originalillustrationen je Handlung statt unpassender alter Bildmontagen erzeugen.
5. **Keine öffentliche TikTok-Veröffentlichung**, kein Merge in Main, keine laufenden kostenpflichtigen Verträge.

## Nächster Schritt
Die Nutzerpräferenz zur Sprecherin und die Abspielbarkeit von MP3 versus MP4 auswerten. Anschließend die gewählte Stimme als feste Serienidentität konfigurieren und einen vollständigen, technisch und redaktionell kontrollierten Testfilm rendern.

## Verbindliche Entscheidung des Nutzers (nach Hörproben)
- **Stimme Nr. 3: Sulafat** ist vom Nutzer ausdrücklich ausgewählt und mit „passt optimal“ bewertet.
- Sie ist die **fest eingestellte Erzählerin für Jori & Flimm**, nicht die frühere Victoria oder Kerstin.
- Jori-&-Flimm-Story-Preview-Compiler setzt ab sofort Gemini TTS 3.8, `speaker_id: Sulafat`.
- Vollständiger Episoden-002-Sulafat-Test: [GitHub Actions Run 39685764672](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39685764672); Ergebnis und mobile tatsächliche Hörbarkeit erst nach Prüfung bestätigen.
- Nicht mit MOTUS vermischen. Keine Veröffentlichung ohne separate Kanalanbindung und erfolgreiche menschliche/technische Qualitätsprüfung.

## Sulafat Full-Episode Verification
- Explicit user selection: **voice 3 / Sulafat** is the desired warm storyteller voice for this project.
- Selected in `scripts/compile_preview_episode.py` and CI test, and assigned to Episode 002 preview payload.
- GitHub Actions rendering: [Run 39685764672](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39685764672), **success**; TTS generated using Gemini 3.8 Flash TTS / Sulafat, subtitles, 1080x1920 H.264 + AAC.
- Real QC: **98.61 seconds**, final-audio loudness **-14.12 LUFS**, true peak **-2.93 dBTP**. Measured on final deliverable.
- Direct playback deliverables generated and verified: `Jori_Flimm_Folge_002_Sulafat_Omi_iPhone.mp4` (720x1280, H.264/AAC, 11.4 MB) and `Jori_Flimm_Folge_002_Sulafat_Nur_Ton.mp3` (mono, 1.9 MB). These are ChatGPT conversation artifacts, not persisted GitHub media.
- This is a **PREVIEW_ONLY** video using reused artworks, not verified new scene-specific illustrations. Its publishing flags are false; no TikTok post; no MOTUS change.
- The user still must judge practical handset loudness of the full MP4; a loudness measurement cannot guarantee local playback volume.
