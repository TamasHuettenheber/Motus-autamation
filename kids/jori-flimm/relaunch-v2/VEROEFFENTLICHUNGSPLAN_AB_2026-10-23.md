# Jori & Flimm – verbindlicher Tagesrhythmus und Veröffentlichungsvorbereitung
Stand 22. Oktober 2026

## Beschluss des Nutzers
**Nicht fünf Beiträge am selben Tag.** Erstveröffentlichung Folge 001 **23.10.2026 um 14:00 Uhr Europe/Berlin**, danach **jeden weiteren Tag genau eine Folge** auf dem **separaten TikTok @jori.flimm**. MOTUS bleibt unberührt.

| Folge | Veröffentlichungsdatum | Lokal | Buffer UTC `dueAt` | tatsächlicher Buffer-Status |
|---:|---|---|---|---|
| 001 | Fr 23.10.2026 | 14:00 CEST | 2026-10-23T12:00:00Z | geplant, **nicht erstellt** |
| 002 | Sa 24.10.2026 | 14:00 CEST | 2026-10-24T12:00:00Z | geplant, **nicht erstellt** |
| 003 | So 25.10.2026 | 14:00 CET | 2026-10-25T13:00:00Z | geplant, **nicht erstellt** |
| 004 | Mo 26.10.2026 | 14:00 CET | 2026-10-26T13:00:00Z | geplant, **nicht erstellt** |
| 005 | Di 27.10.2026 | 14:00 CET | 2026-10-27T13:00:00Z | geplant, **nicht erstellt** |
| 006 | Mi 28.10.2026 | 14:00 CET | 2026-10-28T13:00:00Z | noch keine fertig produzierte Folge |
| 007 | Do 29.10.2026 | 14:00 CET | 2026-10-29T13:00:00Z | noch keine fertig produzierte Folge |
| 008 | Fr 30.10.2026 | 14:00 CET | 2026-10-30T13:00:00Z | noch keine fertig produzierte Folge |

**Sommerzeit endet 25.10.2026.** Unbedingt `Europe/Berlin` und Buffer `dueAt` mit dynamischem UTC-Offset nutzen.

## Verifizierte Buffer-Verbindung
- Bereits vorhandenes GitHub-Actions-Secret `BUFFER_API_KEY`, kein zweiter API-Schlüssel erforderlich.
- Read-only GitHub-Actions-Lauf **39694571119** bestätigt den ausschließlich richtigen TikTok-Kanal **@jori.flimm**.
- Jori-Buffer-Warteschlange zu diesem Zeitpunkt: **0 geplante Posts**. Kein Schreibzugriff auf MOTUS ausgeführt.
- Das JSON `buffer_folgen_001_005_entwuerfe.json` enthält die fünf getrennten 14-Uhr-Termine, IDs und Captions. `scheduled_in_buffer:false` bedeutet ausdrücklich: **keine Buffer-Termine gebucht**.

## Rollierende Produktion ab Folge 006
**Vorlauf drei volle Kalendertage – statt Produktion kurz vor Posting.**
- Für jede zu veröffentlichende Folge `N` steht ihr Datum `D` fest: 14:00 Europe/Berlin, beginnend 28. Oktober für Folge 006.
- **D−3 um 20:00:** neue Fortsetzungsgeschichte schreiben; direkt an vorherigen Cliffhanger anknüpfen; Dubletten und Buch-Spoiler verhindern. Beispiel Folge 006: **25.10. 20:00**.
- **D−3 um 20:30:** sechs handlungsgenaue Originalbilder, Sulafat-Stimme, exakt sieben Sekunden Rätselpause und Video schneiden.
- **D−3 um 21:30:** echte Bild-/Text-/Sprachsynchronisation, Rätselhinweise, Cliffhanger, Lautheit und komplette Sicht-/Hörprüfung.
- **D−1 spätestens 19:00:** spätestens jetzt muss der fertige Film mit Freigabe und stabiler HTTPS-Medienadresse in Buffer für Tag D um 14:00 fest eingeplant sein.
- Zielbestand: mindestens **drei vollständig freigegebene, bereits eingeplante Folgen**, maximal nach Kapazität (Buffer Free: zehn geplante Posts pro Kanal).
- Nach erfolgreich versendeter Folge und tatsächlicher TikTok-URL die Zählung in der Jori-Serienhistorie fortschreiben; **nicht** beim bloßen Rendern oder beim Schieben in die Queue.

## Was technisch vorbereitet wurde
1. `scripts/rolling_calendar.py` berechnet alle Folgetermine mit DST, Veröffentlichungsabstand und dreitägigem Vorlauf. `test_rolling_calendar.py` blockiert Doppeltermine und falsch als veröffentlicht ausgewiesene Beiträge.
2. `scripts/generate_episode.py` berücksichtigt nun die echten ersten fünf Neustartfolgen als bestehende Handlung und arbeitet ab **Folge 006** weiter, ohne noch einmal das erste Kennenlernen oder bereits benutzte Rätsel zu erzählen. Test/CI: nächster Entwurf ist `e006` für `2026-10-28`.
3. `.github/workflows/jori-relaunch-rolling-draft.yml` enthält einen optionalen **20:00 Europe/Berlin** GitHub-Action-Zeitplan für den nächsten dreitägigen Story-Entwurf. **Nicht aktiv**: er wird nur auf der Standardbranch und bei freigeschalteter Repository-Variable `JORI_RELAUNCH_AUTO_DRAFTS=true` gestartet. Kein Merge durchgeführt.
4. Post-Texte als getrennte Entwürfe gespeichert, nicht veröffentlicht.

## Freigabeblocker und ehrlicher Status
- Die fünf vorhandenen MP4-Dateien sind **Arbeitsfassungen**, keine final geprüften/abgenommenen Videos. Untertitel nur teilweise als Handlungstafeln, nicht vollständig wortgenau synchron; Szenenbilder zum Teil alte Illustrationen; iPhone-Hör-/Sichttest fehlt. Der Nutzer hat die vollständige QC **zwingend** verlangt.
- Die bisherigen ChatGPT-Bibliotheksdateien und GitHub-Actions-Artefakte sind **keine dauerhaften direkten öffentlichen Video-URLs**, die Buffer für die automatische Videopublikation benötigt. Stabiles HTTPS-Medienhosting muss vor dem ersten echten Posting eingerichtet und verifiziert sein.
- Eindeutiger Buffer-Kanal plus API-Schlüssel sind **schon vorhanden**. Nutzer muss hierfür keinen weiteren API-Schlüssel erstellen.
- Kostenfreie Sulafat-TTS zeigte HTTP 429 bei parallelen Anfragen; in der Produktionskette nur **sequenzielle Generierung**, vernünftige Cooldowns und bei Quota-Problemen **Stopp statt Stimme wechseln oder bezahlen**.
- Auto-Bildgeneration, vollständiger Untertitel-Alignment-Test und telefonische Endabnahme sind nicht automatisiert. **Keine Veröffentlichung vor erfolgreichem vollem QC-Nachweis.**
- Der Termin 23.10.14:00 ist der gewünschte Starttermin, aber aktuell **nicht als sicher gebuchte Veröffentlichung zu bestätigen**. Bestehende fehlerhafte Testfassungen ungeprüft einzuplanen wäre ein Verstoß gegen die festgelegten Serienregeln.

## Nächste Schritte
A. Für Folge 001 zuerst handlungsgenaue Bilder, echte Sprach-/Untertitel-Ausrichtung, komplette Ton-/Bild-Review und iPhone-Kontrolle fertigstellen.
B. Eine stabile, öffentlich erreichbare MP4-Datei hosten und als Private/Entwurfstest über den exakt richtigen Buffer-Kanal prüfen.
C. Erst bei bestandener Freigabe **genau eine** Folge am jeweils zugehörigen Datum um 14:00 Uhr einplanen. Rückmeldung mit tatsächlicher Buffer-Post-ID und anschließend öffentlichem TikTok-Link.
D. Pipeline fürs selbstständige Bild-/Video-Rendering, Fehlerrückmeldung und den dreitägigen Puffer fertigstellen, danach erst GitHub-Zeitsteuerung aktivieren.

MOTUS hat eigene Jobs, Konten und Postingrhythmen und darf nicht geändert werden. Keine kostenpflichtige Subscription.
