# Jori & Flimm – Produktionsstand 23.10.2026

## Tarifprüfung für Sulafat-TTS
- Im Repository ist für die Folgen 002–005 `gemini-3.8-flash-lite-tts` gesetzt. Das Skript nennt es „Free-Tier TTS“, diese Bezeichnung allein belegt aber nicht den Tarif des verwendeten Projekts.
- Die offizielle Google-Preistabelle führt für `gemini-3.8-flash-lite-tts` im **Standard-Free-Tier** Text-Eingabe und Audio-Ausgabe als kostenlos. Batch und Flex sind im Free Tier nicht verfügbar; Paid-Tier-Raten sind separat aufgeführt. Quelle: [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing).
- Google weist darauf hin, dass der Projekt-Tarif in AI Studio unter **Projects → Billing Tier** erscheint. Quelle: [Google Gemini API billing](https://ai.google.dev/gemini-api/docs/billing).
- **Tarif des konkreten Projekts: nicht verifiziert.** Der lesende Zugriff auf den verbundenen Opera-Browser verlangte Reauthentifizierung; ein AI-Studio-/Google-Cloud-Billing-Connector steht nicht zur Verfügung.
- Die frühere Projektklärung (21.10.) bestätigte die Absicht, im kostenlosen Tarif zu bleiben, und dass Flash-Lite eine kostenlose Nutzungsstufe hat; ein tatsächlicher Nachweis der Billing-Tier-Anzeige des konkreten Projekts ist in den bisherigen Chats/Projektdateien nicht dokumentiert. Erfolgreiche API-Aufrufe belegen nur den Zugang, nicht die Billing-Stufe.
- Der Gemini-Schlüssel wurde laut Projektverlauf auch für MOTUS-TTS genutzt. Google limitiert Gemini API pro Projekt, nicht pro Schlüssel; gemeinsamer Verbrauch kann den 429 erklären, ist aus den vorliegenden Logs aber nicht bewiesen. Quelle: [Google rate limits](https://ai.google.dev/gemini-api/docs/rate-limits).
- Die TTS-Fehlerbehandlung wurde am 23.10. angepasst, damit künftige Action-Logs Googles strukturierte Status-/Quota-Details zeigen, ohne Schlüssel oder Request-Header zu protokollieren: [Commit 4783c300](https://github.com/TamasHuettenheber/Motus-autamation/commit/4783c300b3c5c394a5d4e964371ecbd8c767e58e). Die Änderung wurde nicht ausgeführt; es gab keinen weiteren TTS-Aufruf.
- Die erfolgreiche TTS-Ausgabe in GitHub Action [39753201500](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39753201500) und HTTP 429 in [39836089743](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39836089743) beweisen den Projekttarif nicht.
- In diesem Lauf wurde kein Google-TTS-Aufruf, kein Render und keine Buffer-Buchung ausgelöst. TTS bleibt gesperrt, bis der konkrete Projekt-Tarif als Free bestätigt ist.

## Folge 006 – „Der Ton im Glashaus“
- Storyentwurf: [episode_006_story_draft.json](../relaunch-v2/episode_006_story_draft.json). Er setzt direkt beim riesigen Fußabdruck und Sterngeheimnis aus Folge 005 an.
- Neues Klang-/Echo-Rätsel mit drei unterschiedlich langen Glasröhren; eine Frage, ein Marker `[[PAUSE:7]]), Auflösung, Handlungsfortschritt und neuer Cliffhanger.
- Story-QC: Jori ist durchgehend weiblich referenziert; Rätseltyp unterscheidet sich von 001–005. Die sieben Sekunden sind im Text markiert, aber ohne TTS/MP4 noch nicht als echte Audiostille geprüft.
- Fünf neue Szenenbilder: [assets/episode-006](../relaunch-v2/assets/episode-006/): Fußabdruck am Berghang, Glashaus außen, Klangröhren, Lösung/Teleskop, Sternkarten-Cliffhanger. Alle sind 941×1672 px (nahe 9:16) und visuell unterschiedliche Kompositionen.
- Sichtprüfung am 23.10.: alle fünf tatsächlichen PNGs geöffnet; je eigenes Motiv und folgenspezifischer Hintergrund, Jori/Flimm konsistent, Reihenfolge passt zur Handlung. Die Rätselhinweis-Karten müssen im Renderer als lesbarer Overlay eingeblendet werden; sie sind nicht in die Bilder eingebrannt.
- Live-Zugriffsprüfung: Google AI Studio `/api-keys` leitete im verfügbaren Browser auf die Google-Kontoauswahl weiter; kein angemeldeter AI-Studio-Zugriff und daher dort keine Billing-Tier-Anzeige sichtbar. Es wurde kein TTS-Aufruf ausgelöst.
- Render-QC, Untertitel-Timing, Sulafat-Audio, MP4-Spuren/Dauer und sieben Sekunden Stille: offen, weil noch keine Folge-006-MP4 erzeugt wurde.
- Produktionsweg-Prüfung am 23.10.: vorhandener `github_followup_renderer.py` und `github_followup_buffer.py` akzeptieren fest nur Folgen 002–005 und lesen deren alte JSON-/JPG-Pfade. Folge 006 braucht daher eine gezielte Jori-only-Erweiterung von Voice-Wrapper, Renderer (PNG-Motive + Klanghinweise) und Buffer-Helfer, bevor ein kontrollierter GitHub-Lauf möglich ist. Die MOTUS-Dateien bleiben unberührt.
- Buffer: kein neuer Post; Post-ID/Status/Termin nicht vorhanden. Der nächste Termin nach den bisher belegten Folgen 001–005 wäre vorläufig 27.10.2026, 14:00 Europe/Berlin; vor einer Buchung ist der Live-Buffer-Stand erneut zu prüfen.

MOTUS-Dateien und -Workflows wurden nicht verändert.
