# Folge 001 – konkrete Nutzerkritik und überarbeitete Vorschau V3

Stand 22.10.2026. **Nicht zur automatischen Veröffentlichung freigegeben.**

## Nutzerfeedback aus der tatsächlich angehörten Arbeitsfassung
1. Das bisherige Rätsel wird durch große Textfelder/Board-Grafik vermittelt und verdeckt die eigentlichen Illustrationen.
2. Der gesprochene Sprechertext ist nicht als mitlaufender Text lesbar; stattdessen standen dort nur grobe, teils ganz andere Texttafeln.
3. Es gibt keinen klar erkennbaren gesprochenen Serienauftakt mit **Folge 001**. Der Hook setzt zu plötzlich und ohne Rahmen ein.

## Umgesetzt in neuer Datei V3
- Als erstes neuer, original von **Sulafat** gesprochener Auftakt: „Jori und Flimm. Folge eins: Das Licht, das Joris Namen kannte.“ Gemini-Flash-TTS-Run [39737646347](https://github.com/TamasHuettenheber/Motus-autamation/actions/runs/39737646347). Das Intro dauert 7,84 s und ist bewusst vor den bestehenden Hook gesetzt.
- **Nur eine kleine Staffel-Kennzeichnung oben**, normale Storybilder füllen wieder fast das ganze 720×1280-Hochformat.
- Drei **kleine holzähnliche Wegweiser im Motiv** (MOND, SONNE, STERN), keine große dunkle Drei-Spalten-Quiztafel; Hinweise vom ersten Sprechen über die Wegweiser bis nach der Rätselpause sichtbar.
- Als Untertitel werden jetzt **alle gesprochenen Wörter** als kurze passende 1–2-Zeilen-Einblendungen gezeigt, einschließlich des neuen Serienauftakts. Der exakte Wortlaut in den Karten stimmt vollständig mit dem zugrunde gelegten Originalskript überein (151 Wörter, tokenisierte Übereinstimmung 100 %, die Frage ist während der Rätselpause bewusst zweimal in den Subtitle-Events enthalten).
- Die Rätsel-Frage bleibt während der vollständigen Pause sichtbar; Lösung erscheint danach.
- Originalaudio aus den beiden **Sulafat**-Quellen zusammengesetzt: `Jori_001_Sulafat_Serienauftakt.wav` und `folge_001.wav`. Keine Sprecherinnenänderung.
- MP4: 720×1280 H264/AAC, **93,68 s**, ~5,2 MB. Tonmessung am fertig gerenderten MP4: ca. **−14,69 LUFS**, true peak **−1,06 dBTP**. Audio-Silence-Detektor erkennt eine zusammenhängende Denkpause von **7,49 s** (in Quellaudio exakt sieben Sekunden Stille, mit natürlicher Pause vor und nach).
- Neue MP4 liegt als persönliches Nutzerartefakt in ChatGPT-Bibliothek: `/Jori & Flimm/Staffel 1/Jori_Flimm_Folge_001_Neu_V3_Sprechertext_und_Raetsel.mp4`; alte Version nicht überschrieben.

## Noch offen / nicht behaupten
- **Untertitelzeitstempel basieren auf manueller Satz-/Silence-Annäherung**, nicht auf einem nachgewiesenen Wort-für-Wort-ASR-Alignment. Ihr Vollständigkeits-/Wortlautcheck ist bestanden, aber die zeitliche Synchronität benötigt einen vollständigen Hörtest und idealerweise Forced Alignment. Nicht als final abgenommen deklarieren.
- Keine individuell komplett neu illustrierten sechs Szenen; vorhandene Jori/Flimm-Illustrationen mit kleinen echten Rätselobjekten kombiniert. Bei Änderung neue QA.
- Kein unabhängiger iPhone-Handytest durch Nutzer für diese neue Version.
- Kein Upload von V3 in öffentliche Buffer-Medien-URL, keine Buffer-Post-ID, keine TikTok-Veröffentlichung. Qualitäts-Sperre bleibt aktiv.
- Neue Folge 001 zeigt jetzt „Folge 001“ und liest diesen Auftakt vor; Nutzerfeedback zur neuen Fassung abwarten, bevor dieselben Korrekturen auf Folgen 002–005 angewendet werden.

## Verbindliche Ergänzungen an die künftige Render-Pipeline
1. Serienauftakt pro Folge am Anfang hör- und sichtbar mit fortlaufender Nummer, aber nicht als langes Werbe-Intro. Auf Folge 001 echte Einführung der Figuren; ab 002 immer direkte Fortsetzung.
2. Keine großflächigen, undurchsichtigen Boards/Tafeln, die ganze Szene verdecken. Rätselhinweise als in die gezeichnete Welt integrierte Gegenstände und Symbole, die die Kinder deutlich erkennen können.
3. Ausschließlich Untertitel, die das **tatsächlich Gesprochene** enthalten, zeitlich in 1–2 kurze Zeilen aufgeteilt, niemals allgemeine Text-Placeholders. Lesbare helle Schrift mit Kontur innerhalb sicherem unteren Bereich (nicht TikTok-UI überdecken).
4. Während der sieben Sekunden komplett stillen Rätselpause exakt dieselbe Frage und die sichtbaren Hinweise stehen lassen.
5. Jede Folge vor Upload gegen vollständiges Audio und jedes tatsächliche Bild und gegen den direkten Nachfolger-Cliffhanger prüfen; QC-Fehler blockieren die Veröffentlichung.
