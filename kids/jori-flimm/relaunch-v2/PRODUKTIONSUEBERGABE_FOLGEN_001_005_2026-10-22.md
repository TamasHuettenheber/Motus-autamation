# Jori & Flimm – Produktionsübergabe 22.10.2026

## Erfolgreich und durch Buffer bestätigt
GitHub-Actions-Lauf: https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39753201500

| Folge | Termin Europe/Berlin | Dauer | Buffer-Post-ID | Status |
| --- | --- | --- | --- | --- |
| 001 | 22.10.2026 14:00 | 104,28 s | `6ad9ce4baefa17e341f96c3f` | scheduled |
| 002 | 23.10.2026 14:00 | 81,36 s | `6ad9d2f9a013397d9328faea` | scheduled |
| 003 | 24.10.2026 14:00 | 79,12 s | `6ad9d321a013397d932908dc` | scheduled |
| 004 | 25.10.2026 14:00 | 80,68 s | `6ad9d34aaefa17e341fad444` | scheduled |
| 005 | 26.10.2026 14:00 | 79,16 s | `6ad9d373e6aee73a2b15d107` | scheduled |

Alle Buffer-Post-IDs stammen aus tatsächlichen `JORI_BUFFER_SCHEDULED_CONFIRMED`-Rückgaben. Das bestätigt die Planung, nicht die spätere Veröffentlichung auf TikTok.

### GitHub-Pipeline
- `.github/workflows/jori-v10-github-buffer.yml` für Folge 001.
- `.github/workflows/jori-followups-fast.yml` für Folgen 002–005, bereits erfolgreich.
- `kids/jori-flimm/relaunch-v2/scripts/github_followup_voice.py` korrigiert Joris weibliche Pronomen in den gesprochenen Texten und generiert Sulafat-TTS.
- `kids/jori-flimm/relaunch-v2/scripts/github_followup_renderer.py` rendert 9:16 MP4 mit episodenbezogenen Rätselmotiven, Untertiteln und 7 Sekunden Rätselpause.
- `kids/jori-flimm/relaunch-v2/scripts/github_followup_buffer.py` prüft den eindeutigen TikTok-Kanal @jori.flimm, den öffentlichen MP4-Link und vorhandene Planungen, bevor ein neuer Buffer-Post angelegt wird.
- Render-MP4s unter `published/jori-flimm-2026-10-XX-e00X.mp4` auf Jori-Feature-Branch.
- MOTUS nicht verändert. Keine Metricool-Veröffentlichung.

### Offen
- TikTok-Livecheck nach den jeweiligen 14-Uhr-Terminen.
- **Folge 006 und danach**: Noch keine vollautomatische fortlaufende Render-/Buffer-Pipeline. Bisher sind 001–005 eingeplant.
- Die Folgen 002–005 verwenden bestehende Jori-/Flimm-Illustrationen mit jeweils speziell gerenderten Rätselmotiven; eine eigenständige Bildgeneration je Folge ist noch nicht integriert.
- Der ursprüngliche langsame Ubuntu-apt-Workflow wurde aus dem Branch entfernt; der erfolgreiche schnelle Workflow bleibt.
