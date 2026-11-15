# MOTUS – Technik & Reparatur: Arbeitsstand

## MOTUS-T-20261115-LIVE01
**Besitzer:** MOTUS – Technik & Reparatur  
**Status:** ERLEDIGT (Liveprüfung nach eingegrenzter Scheduler-Verzögerung)  
**Geprüft:** 2026-11-15T08:25:52.855823+00:00 (09:25 Europe/Berlin)

**Ursache/Ausgangslage:** Der stündlich konfigurierte GitHub-Buffer-Monitor (`cron: 7 * * * *`) hatte nach dem Lauf 2026-11-15T01:46:48Z bis nach Fälligkeit des 07:00-MOTUS-Slots keinen neuen nachweisbaren Lauf. Snapshot 01:48:43Z war vor Fälligkeit und deshalb **keine Ausfallbestätigung**.

**Maßnahme:** Einmaliger read-only Statusabruf durch bestehenden Buffer-Status-Monitor, ausgelöst durch dokumentarische Anmerkung an `.github/workflows/buffer-monitor.yml`, Commit `97fb28755cfcee4d58e9e15641ceed44b8125b07`. Der vorhandene Workflow-Lauf [43694279847](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/43694279847) wurde erfolgreich abgeschlossen; `diagnostics/buffer-status.json` wurde aktuell zurückgelesen (Blob `73287714ec188ee4b20b2f72361048961fe1255a`).

**Zielnachweis:** Post `6af799614b28296eb11f951e`, `dueAt=2026-11-15T06:00:00Z`, `status=sent`, `sentAt=2026-11-15T06:02:20.759Z`, [externer TikTok-Link](https://tiktok.com/@motus614/video/7708274118784797985). Drei restliche Slots am 15.11. und vier Slots am 16.11. einmalig als `scheduled` mit korrektem `dueAt`; acht MP4 in `published/` mit GitHub-Tree-SHA und Größe vorhanden; Tagesaufträge #107/#108 mit QC-/Renderer-Abschluss. Keine Zusatzproduktion, keine Poständerung.

**Zugriff:** GitHub-Fachzugang bestätigt. Browser-Connector fehlte der originating browser context; dies ist keine belegte Workstation-Sperre. Desktop Commander zeigte nur die verbotene Rezeption, die nicht genutzt wurde. Technisches AgentMail-Postfach nach aktuellen technischen Meldungen geprüft; keine neue inhaltliche externe Behördenantwort. Die einmal tägliche Behördenprüfung nach 11 Uhr war zu dieser Prüfzeit noch nicht fällig.

**Ablage:** Zwei konkrete Library-Zielpfade (`/Hüttenheber Digital/01_Agenten/` und `/Motus/`) wurden versucht; beide Uploads `AccessDeny: id=None`. Die dortige Ablage wurde **nicht** als erfolgt gewertet. Dieser separate GitHub-Reparaturstand dient als erreichbares technisches Ersatzprotokoll; die zentrale `START_HIER_Agent_Economy.md` bleibt unverändert.

**Nächste Voraussetzung:** Bei künftigen Fälligkeiten aktuelle Buffer-`checked_at`-Werte, `postId`, `dueAt`, `status` und `externalLink` abgleichen. Vor etwaiger Recovery nachweislich fehlgeschlagene Stufe sowie aktuelle MP4/QC und Duplikatstatus feststellen. Laufende Monitor- oder Recovery-Run-ID nicht duplizieren.

## MOTUS-T-20261115-PD422
**Besitzer:** MOTUS – Technik & Reparatur  
**Status:** EXTERNER_TRIGGER_UNGEKLÄRT / KEIN NACHGEWIESENER TAGESAUSFALL  
**Prüfstand:** 2026-11-15, Buffer-Zielabfrage 17:57:32Z; technischer Vorgang vom 15.11. 14:38:58 GMT  

**Neuer Eingang:** Pipedream-Fehlermeldung zum Workflow `Motus GitHub Trigger (p_V9Cwrak)` vom 15.11. um 14:38:58 GMT; GitHub antwortete auf einen Workflow-Dispatch mit HTTP 422 `Required input 'text' not provided`. Original: Library `/Motus/[pipedream] Error in workflow Motus GitHub Trigger (p_V9Cwrak) at 2-38-58 PM GMT.pdf`. Der API-Request wurde zurückgewiesen; aus dieser Meldung folgt **kein** gestarteter Renderer oder fehlgeschlagener regulärer Tagesauftrag.

**Ursachenprüfung:** Die bestehende `.github/workflows/motus.yml` verlangt `workflow_dispatch.inputs.text.required: true`; der Dispatcher muss ein nichtleeres `text` je beabsichtigtem Auftrag übergeben. Der reguläre Produzent `motus-night-production.yml` und Batch-Dispatcher `motus-day.yml` verwenden die validierten Texte aus dem jeweiligen Tages-Issue; sie gehören nicht zur Pipedream-Fehlermeldung. Der Tagesauftrag #107 (15.11.) und #108 (16.11.) sind geschlossen mit `MOTUS_DAY_COMPLETE`, vier erfolgreichen Renderer-/QC-Slots je Tag. Es wurde **keine** ungesicherte Annahme getroffen, welchen Event-Payload der externe Pipedream-Trigger tatsächlich erhalten hat.

**Aktueller Zielnachweis:** `diagnostics/buffer-status.json`, `checked_at_utc=2026-11-15T17:57:32.210039+00:00`, bestätigt am 15.11. 07:00 (`6af799614b28296eb11f951e`), 12:00 (`6af799a778196a0a9728e986`) und 18:30 (`6af79968d16af15d4ddc4003`) jeweils `sent` samt externem TikTok-Link. 15.11. 22:00 (`6af799b0bb36d00909d4730b`) sowie alle vier Slots am 16.11. stehen jeweils einmalig auf `scheduled` mit richtigem `dueAt`; keine doppelten `dueAt` im geprüften Tagesumfang. Acht MP4-Dateien im `published/`-Tree vorhanden. Der 22:00-Slot liegt zur Prüfzeit noch in der Zukunft, also keine Publikationsaussage.

**Versuchte autorisierte Wege:** Aktuelles GitHub-Workflow-Schema und Tages-Issues/Kommentare ausgelesen; originalen Pipedream-Fehler geprüft; Browser-Connector scheitert konkret mit `originating browser context`; Desktop-Commander-Auflistung enthält nur `Rezeption` (verboten, nicht genutzt). Dieser Befund beweist **nicht**, dass die vom Nutzer genannte ChatGPT-Workstation generell unverbunden wäre. Es wurde kein zusätzlicher Dispatch, Issue, Renderer, Buffer-Post oder API-Test erzeugt, und das schützende GitHub-Pflichtfeld `text` wurde **nicht** abgeschwächt.

**Nächste Voraussetzung:** Falls der Pipedream-Trigger weiterhin als aktiver Bestandteil vorgesehen ist, seinen konkreten ausgehenden Dispatch-Payload und die Event-Mapping-Konfiguration über einen tatsächlich autorisierten Pipedream-/Workstation-Zugang lesen. Dann ausschließlich die fehlerhafte Abbildung zu `inputs.text` korrigieren, mit isoliertem Mappingtest ohne Live-Video-Dispatch. Keine Wiederholung dieses Diagnoseschritts ohne neue Zugangsvoraussetzung. Das reguläre GitHub-System weiter anhand aktueller MP4/QC-, Buffer- und Veröffentlichungsnachweise prüfen.

## MOTUS-T-20261115-NIGHT-SCHEDULE
**Besitzer:** MOTUS – Technik & Reparatur  
**Status:** BEOBACHTUNG / GitHub-Zeitplan verspätet; kein belegter Produktionsausfall  
**Prüfzeit:** 2026-11-15, ca. 22:57 Europe/Berlin (21:57 UTC, Laufkontext)

**D und D+1:** Der aktuelle Buffer-Nachweis `diagnostics/buffer-status.json` mit `checked_at_utc=2026-11-15T21:42:46.913955+00:00` bestätigt alle vier Beiträge des 15.11. als `sent` mit echten TikTok-Links. Der neu bestätigte 22:00-Slot: `postId=6af799b0bb36d00909d4730b`, `dueAt=2026-11-15T21:00:00Z`, `sentAt=2026-11-15T21:02:57.370Z`, `externalLink=https://tiktok.com/@motus614/video/7708506310077140256`. Die vier 16.11.-Slots sind einmalig als `scheduled` mit korrektem `dueAt` im aktuellen Snapshot enthalten; vier MP4-Dateien des 16.11. haben positive Größe im `published/`-Tree. Keine Recovery erforderlich.

**D+2:** Der reguläre Erzeugungszeitpunkt 22:37 Europe/Berlin war überschritten. Eine exakte GitHub-Issue-Suche nach `[MOTUS-DAY] 2026-11-17` ergab zum Prüfzeitpunkt keinen Treffer. Die aktuelle Workflow-Run-Liste enthielt keinen neuen `MOTUS Night Production`-Run nach dem Lauf `43755289181` (19:57:27 UTC); dieser gab `OUTSIDE_NIGHT_WINDOW` um 20:57 MEZ aus. Der Workflow definiert den regulären Cron 21:37 UTC sowie einen 15-Minuten-Cron und prüft das Nachtzeitfenster selbst. Es liegt bisher kein gescheiterter Produzent-Lauf für 17.11. vor. Deshalb **keinen** eigenen Tagesauftrag und **keinen** zusätzlichen regulären Dispatch erstellen. Beim folgenden vorhandenen GitHub-Lauf die Erstellung und den tatsächlichen Batch-/Render-/QC-/Buffer-Zielzustand für 17.11. prüfen. Erst konkrete Ausfallgefahr / gescheiterte Stufe nachweisen, bevor eine bestehende Recovery eingesetzt wird.

**Zugriff / Postfach:** GitHub-API und AgentMail berechtigt. Browser-Connector konkret mit `originating browser context` gescheitert; Desktop Commander listete nur die ausdrücklich verbotene Rezeption (nicht verwendet), was die Nutzeraussage zur ChatGPT-Workstation weder bestätigt noch widerlegt. AgentMail-Suchen nach Finanzamt, Gewerbeamt und Steuer/Finanz ab 10.11. lieferten keine neue inhaltliche Antwort. Pipedream-422-Vorgang unverändert; keine erneute erfolglose Anmeldungs-/Mappingprobe.

**Nächste Voraussetzung:** Nächsten tatsächlichen Night-Producer-Run mit Issue für 17.11. abgleichen; bei neuem Fehler Ursache, Run-ID und fehlgeschlagene Stufe belegen. Bereits veröffentlichte oder eingeplante Beiträge nicht verändern.

