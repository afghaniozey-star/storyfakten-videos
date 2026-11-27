# Täglicher Ablauf (gestartet um 09:34 Berlin – Stadt muss bis 13:00 fertig sein)

## 0. Einrichtung in einer frischen Sitzung (ZUERST, dauert ~10–20 min)
Das Setup-Skript der Umgebung installiert absichtlich nur Kleinkram (sonst bricht es wegen Zeitlimit ab).
Die Stimme (OmniVoice, ~6 GB + Modell 3 GB) installierst du selbst – **im Hintergrund** (Bash mit run_in_background), während du Themen recherchierst:
```bash
bash pipeline/setup.sh > ~/setup.log 2>&1; echo FERTIG >> ~/setup.log
```
Fertig, wenn `~/setup.log` "FERTIG" und "bereit" enthält. Danach gibt es `/opt/omni/venv` (OmniVoice), `piper`, `faster-whisper`, `ffmpeg`, `npx hyperframes`.
Scheitert es (z. B. gesperrte Adresse), dem Nutzer sofort per Push-Nachricht melden, mit der genauen Fehlermeldung.

## 1. Drei Videos pro Tag – Aufgaben an die Helfer-Agenten verteilen
Es gibt fünf Helfer (Ordner `.claude/agents/` im Zweig `main`, als Subagent über das Agent-Werkzeug aufrufen), in dieser Reihenfolge:
1. **`analyse`** – wertet die letzten Videos über Buffer aus (Aufrufe, Likes, Kommentare pro Uhrzeit/Thema/Format) und schreibt Regeln in `pipeline/erkenntnisse.md`.
2. **`trend-scout`** – schaut, welche Video-Formate gerade Trend sind und wie sie gestaltet sind, bewertet unsere Videos, gibt Gestaltungs-Anweisungen.
3. **`recherche`** – findet die konkreten Themen (unter Beachtung von 1 + 2) und prüft alle Fakten mit Quellen.
4. **`video-produktion`** – baut, schneidet, rendert und prüft jedes Video (mit den Anweisungen aus 1 + 2).
5. **`qualitaet`** – Endkontrolle JEDES fertigen Videos vor dem Einplanen (Länge, Ton, Stimme, Bild, Schluss-Aufruf, Regeln). Nur bei **FREIGEGEBEN** wird eingeplant; bei **GESPERRT** repariert video-produktion (1 Versuch), sonst Push an den Nutzer mit Grund.
Der Haupt-Ablauf (du) verteilt die Aufgaben, gibt die Ergebnisse weiter, lädt hoch, plant in Buffer ein und informiert den Nutzer.
Alles kostenlos: keine bezahlten Tools; vidIQ-Credits NUR für die YouTube-Kommentare der Stadt.

Pro Tag (ab 22.11.2026 – Wunsch des Nutzers: ALLE Videos im Story-Format „In dieser Welt …“, jedes über 1 Minute):
- **TEIL-1-STRATEGIE TikTok + Instagram (Nutzer, 27.11.2026 – dauerhaft):**
  - Jeden Tag 2 Videos (16:30 und 23:30). Normalerweise sind BEIDE ein **neuer Teil 1 mit neuem Thema**.
  - Jedes Teil-1-Video endet gesprochen + eingeblendet mit: **„Folg mir und schreib ‚Teil 2‘ in die Kommentare, dann kommt die Fortsetzung!“**
  - **Teil 2 nur für die besten Teil-1-Videos** (meiste Aufrufe/Kommentare nach 2–3 Tagen; analyse entscheidet), frühestens 2 Tage nach Teil 1, höchstens 1 Teil 2 pro Tag – er ersetzt dann einen der beiden Teil-1-Slots (bevorzugt 16:30). Schwache Teil-1-Videos bekommen KEINEN Teil 2.
  - Liste in `pipeline/story-serien.md` („Teil-1-Liste“) pflegen: welcher Teil 1 wann lief, Aufrufe, ob Teil 2 kommt.
  - **Stil (nur noch dieser auf TT/IG):** absurde Regel „In dieser Stadt …“ + Alltagsthema, das junge Leute kennen (Handy, Sprachnachrichten, Akku, Schule, Gruppenchat, Familie, Oma …), Regel mit klarer Zahlengrenze in den ersten 2 s, Satz 2 „Ich“ gegen zweite Person (beide mit Zahl, geteiltes Bild ab 0,0 s), Erzähler mit früh angedeuteter Schwäche/Geheimnis, Twist trifft ihn selbst, offenes Ende mit Frage, Loop aufs Anfangsbild. Keine Quiz-/Countdown-/Türme-Videos mehr auf TT/IG. Muster = „Sprachnachrichten-Stadt Teil 1“ (bestes Video, siehe erkenntnisse.md „Sonderanalyse 27.11.“).
  - `trend-scout` baut aktuelle TikTok-Trends und Alltagsthemen ein.
- **Wenn ein Video NICHT fertig wird (egal warum: Fehler, Zeit, Nutzungslimit): SOFORT eine Push-Nachricht an den Nutzer mit dem Grund** – und zwar sobald es absehbar ist, nicht erst am Ende. Fertige Videos immer sofort einplanen, nicht auf die anderen warten.
- **Sparsam arbeiten** (das Nutzungslimit des Kontos ist am 27.11. erreicht worden, dadurch fehlte ein Video): analyse + trend-scout kurz halten (je max. ~10 Werkzeugaufrufe), keine unnötigen Testrenders, Standbilder gezielt.
- **Länge 65–80 s** (TikTok zahlt im Creator-Programm nur für Videos über 1 Minute → NIE unter 62 s).
- Format: Vorlage `pipeline/vorlage-story` (Comic-Figuren mit Mimik, Zahlen/Schilder über Köpfen, Kamerafahrten, Untertitel, selbst erzeugte Musik, Ende „TEIL N+1? ➕ FOLGEN“).
  Bausteine aus `tools/story.py` wiederverwenden (person, badge, street_bg, room_bg, cam, expr, pop) und für jede Geschichte neue Szenen-Sets schreiben.
- Geschichten müssen EIGENE Ideen sein – keine fremden Geschichten nacherzählen oder übersetzen.
- **STIL (Referenz des Nutzers vom 21.11., 72-s-Video „In dieser Stadt darf man 6-7 nicht dreimal sagen“):** lustig & absurd statt traurig.
  „In dieser Stadt / Welt …“ + absurde Regel als Hook, Ich-Erzähler, viele Figuren mit kurzen Gags (Kumpel, Oma, Bürgermeister …), Steigerung bis zum großen Chaos,
  Loop-Ende (letzter Satz führt zurück zum Anfang / „noch größer“), Schnitt alle 2–3 s, Kamerawinkel wechseln (Nahaufnahme, von unten, Totale mit Menge),
  Einzelwort-Untertitel in der Bildmitte, kurze Einblendungen oben („2x“, „10/10“, „67 JAHRE“, „XXL“, Uhrzeit). Aktuelle Jugend-Memes erlaubt, aber die Geschichte selbst ist IMMER eigen (nichts nacherzählen).
  Figuren im Klötzchen-Look (eckiger Kopf, eckiger Körper, kräftige Farben, einfache Gesichter mit Mimik) – in 2D mit Schatten zeichnen (kein echtes 3D möglich). Keine Roblox-Logos/-Namen.
  Stimme omni-mann, energischer/schneller (length_scale ~0.9). Musik: IMMER der feste Hintergrund-Sound „In this town – Dreamcore“ (Entscheidung des Nutzers vom 22.11.; Datei `pipeline/sound/bgm-in-this-town.mp3`, liegt in jeder Vorlage als `assets/bgm.mp3`). Die Musik-Skripte (musik.py / story_musik.py) loopen ihn automatisch auf Videolänge – nichts ändern, Datei nicht löschen. Soundeffekte dürfen zusätzlich bleiben.
- **YouTube-Abo-Video = „ABO-WELT“ (ab 23.11., ersetzt die Stadt):** „Jeder Abonnent bekommt ein Land“ – Weltkarte, Kamera fliegt zu jedem neuen Land, Land färbt sich in der Farbe des Besitzers, Namens-Fahne, Zähler „X / 195 Länder vergeben“, lustiger Fakt pro Land, Ende mit Abo-Aufruf. Vorlage `pipeline/vorlage-abowelt` (tools/abowelt.py), Zustand `pipeline/abo-welt/welt.json`. Kreativ: Ereignisse einbauen (zwei wollen dasselbe Land → Duell per Likes; Nachbarn schließen Bündnis; größtes Reich bekommt Krone). Karte: svg-maps (CC BY 4.0) in der Beschreibung nennen. Türme- und Stadt-Videos ruhen.
- **Abo-Welt-Sound:** auch die Abo-Welt benutzt den festen Hintergrund-Sound (assets/bgm.mp3, über tools/story_musik.py).
- **Abo-Text & Aufruf:** Ein Land gibt es nur für Leute, die **abonnieren UND ihr Wunschland kommentieren**. Das in Video (gesprochen + eingeblendet, schon am Anfang) und Beschreibung immer so sagen: „Abonnier und kommentier dein Wunschland – nur Abonnenten bekommen ein Land!“ (Ob jemand wirklich abonniert hat, können wir technisch nicht prüfen – die Regel wird angesagt, nicht kontrolliert.)
- **Story A beginnt immer mit 1 Satz „Was bisher geschah …“**, damit sie auch ohne Teil davor verständlich ist (auf YouTube läuft nur Story A).

## 1b. YouTube-Abo-Welt (Zustand in `pipeline/abo-welt/welt.json`; früher Stadt: `pipeline/stadt-youtube/stadt.json`)
- Kommentare lesen: vidIQ `vidiq_video_comments` mit channelId `UCHkoA2sBD7_hbxF-4et4LLg`, order "time", maxResult 50 – **höchstens EIN Aufruf pro Tag** (5 Gratis-Credits).
  Vorher `vidiq_balance` (kostenlos) prüfen: unter 5 Credits → KEIN Abruf, nur die offenen Wünsche aus stadt.json verwenden. **Niemals Credits kaufen.**
  Bis 30.11.2026 sind nur noch ~10 Credits übrig → Kommentare nur jeden 2. Tag lesen, ab 01.12. täglich.
- Neue Wünsche seit `kommentare_gelesen_bis` in `wuensche_offen` übernehmen (Name = Handle ohne @, max. 12 Zeichen, Großbuchstaben; EIN Land pro Person; Wunschland vergeben → freies Nachbarland; ohne Landwunsch → passendes freies Land wählen; Beleidigungen/Politik ignorieren; bestehende Hauswünsche aus stadt.json dürfen in Länder umgewandelt werden).
- Pro Tag 3–6 Länder vergeben (älteste Wünsche zuerst), in `besitzer` eintragen (land = 2-Buchstaben-Code aus weltkarte.json, land_de, farbe, tag, szene, fakt, ggf. sprechname/fokus), aus `wuensche_offen` entfernen, `tag` +1, `kommentare_gelesen_bis` setzen, committen + pushen.
- Keine echten neuen Wünsche (keine Credits / keine Kommentare) → trotzdem ein Video, aber mit einem EREIGNIS statt neuer Namen. NIEMALS erfundene Namen als Abonnenten ausgeben.
  Ereignis-Ideen (abwechseln): „Wer bekommt Japan?“ (ein Top-Land wird ausgeschrieben – wer zuerst abonniert + kommentiert, bekommt es); Globi (unser Maskottchen, klar erkennbar keine echte Person) schnappt sich ein Land – „Holt es zurück!“;
  Länder-Duell zwischen zwei bestehenden Besitzern um ein Nachbarland (Abstimmung per Kommentar); Rundflug über alle Besitzer mit Zähler + „Noch X frei!“. Immer mit großem Abo-Aufruf.
- Jedes Abo-Welt-Video endet mit dem Abo-Aufruf (Ziel: YouTube-Abos, aktuell ~129).

## 2. FORMAT TÜRME-VIDEOS: TÜRME (Standard – vom Nutzer ausdrücklich gewünscht, wie sein erfolgreiches WM-Finale-Video)
Kugeln mit Augen (Farben/Flagge des Kandidaten) stehen auf Ziegeltürmen. Alle Türme wachsen gemeinsam, bei jedem
„… raus!“ fliegt die Kugel mit dem kleinsten Wert weg. Am Ende **Duell** der letzten zwei („Like für X, Kommentar für Y“),
Pause mit Trommelwirbel, Verlierer raus, Turm des Siegers schießt hoch → Blitz, Krone, Konfetti, Wow-Banner, dann Frage an die Zuschauer.
**Tempo ruhig/langsam** (wie die langsamere WM-Version): pro Ausscheiden ein kurzer Satz („Der FC Barcelona, raus!“) mit ~1 s Pause danach.
KEIN Karten-Countdown mehr (vorlage-countdown nur noch als Reserve).

STIL-REGELN (gelten zusätzlich):
1. **Hook in den ersten 2 Sekunden:** überraschende Behauptung/Frage („90 % tippen hier falsch!“ / „Kleiner Tipp: Nicht Bayern!“).
2. **Spannung:** Ausscheiden vom kleinsten zum größten Wert, eine Zwischenfrage („Na, wer fehlt noch?“), „Jetzt wird's eng“ vor dem Duell. Gewinner erst am Ende.
3. **Zu jedem Kandidaten ein kurzer Fakt** – als Einblendung (`fakt` in tuerme.json), gesprochen nur „X, raus!“.
4. Soundeffekt bei jedem Ausscheiden (macht die Vorlage automatisch), Zahlen/Namen groß.
5. **Musik:** lizenzfrei, selbst erzeugt (`tools/musik.py`, ruft tuerme.py selbst auf), leiser als die Stimme, Steigerung zum Finale.
6. **Ende:** Wow-Vergleich („fast 150 m höher als Platz 2“) + Frage an die Zuschauer + „folg“.
Länge 40–50 s. Keine fremde Musik, keine fremden Clips/Logos/Wappen (nur Farben/Flaggen).

## 3. Video bauen
```bash
cp -r ~/storyfakten-videos/pipeline/vorlage-tuerme ~/v/<thema> && cd ~/v/<thema>
# tuerme.json + voice.json anpassen (Beispiel in der Vorlage: höchste Gebäude). Szenen: s1 (Hook), e1..eN (je ein Ausscheiden),
# s4 (Duell), s5a (Verlierer raus), s5b (Sieger + Zahl + Wow), s6 (Frage + folg)
/opt/omni/venv/bin/python ~/storyfakten-videos/pipeline/stimme-omni/omni_synth.py .   # Stimme omni-mann, ~1 min/Szene
python3 tools/piper_flow.py .        # Wortzeiten
python3 tools/tuerme.py              # Grafik + Musik + Ton
npx -y hyperframes@0.8.228 snapshot --at 1.5,10,20,30,40   # ansehen, Überlappungen beheben
npx -y hyperframes@0.8.228 render -o roh.mp4
ffmpeg -y -i roh.mp4 -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -af "alimiter=limit=0.5:level=false,loudnorm=I=-15:TP=-2:LRA=11,volume=-1dB" -c:a aac -b:a 192k -movflags +faststart final.mp4
```
- tuerme.json: `items` in Ausscheide-Reihenfolge (kleinster Wert zuerst), das vorletzte ist der Duell-Verlierer (`raus.szene` = "s5a"), das letzte der Sieger (ohne `raus`).
  `kurz` = Beschriftung unter dem Turm (max. ~8 Zeichen). `skala.max` etwas über dem Siegerwert, `schritt` für die Hilfslinien.
  `sieger.namewort` / `sieger.zahlwort` und `hook.wort` = Wörter genau wie im gesprochenen Text.
- voice.json: `groups` = [Anzeige, gesprochen], Zahlen gesprochen ausschreiben. Kurze Einzelwörter mit Kontext („Der FC Barcelona, raus!“).
- Prüfen: Whisper-Abschrift gegen Text, Standbilder, keine Überlappungen.

### Stadt-Video bauen (YouTube)
```bash
cp -r ~/storyfakten-videos/pipeline/vorlage-stadt ~/v/stadt && cd ~/v/stadt
cp ~/storyfakten-videos/pipeline/stadt-youtube/stadt.json stadt.json   # Zustand der YouTube-Stadt
```
- `tools/stadt3.py` ist das Beispiel (Tag 3 der TikTok-Stadt, mit Beispiel-Dateien `*-beispiel-tag3.json`): Häuser in Reihen, Sondergebäude (stadion, f1, hangar, bolz,
  feuerwehr, polizei, autohaus, kiosk, pool …), Kamera fährt zu jedem neuen Haus, Namensschild poppt auf. Für den Tag anpassen (neue Sondergebäude ergänzen, z. B. flughafen, krankenhaus).
- Globi (Strichmann) bleibt stumm: `globi.build({}, END, GEST)`. Stimme omni-mann wie bei den Türmen.
- Text: „Tag N in unserer YouTube-Stadt. …“, jeder neue Bewohner mit Namen + Wunsch, Ende: „Kommentier deinen Namen und dein Wunschhaus und abonnier – morgen steht dein Haus!“
- 35–50 s, Musik mit `tools/musik.py`, gleiche Prüfungen wie bei den Türmen.

## 4. Ablage
Zweig `videos`: `videos/JJJJ-MM-TT-<thema>.mp4` committen und pushen. Link siehe CLAUDE.md.

## 5. Einplanen OHNE Freigabe (Anweisung des Nutzers vom 17.11.2026)
Der Nutzer will KEIN „ok“ mehr geben müssen: Sind beide Videos fertig und geprüft, sofort in Buffer einplanen (Abschnitt 6).
Nur wenn eine Prüfung scheitert (Fakt nicht belegbar, Stimme falsch, Video kaputt, Link nicht 200), das betroffene Video NICHT einplanen.
Danach Push-Nachricht an den Nutzer: was wann wo eingeplant ist, Thema, Hook-Satz, Quellen, Videos als Anhang (SendUserFile) – und was ggf. nicht geklappt hat.
Wird 16:30 knapp, Video 1 zum nächsten freien Termin am selben Tag einplanen (nie in der Vergangenheit).

## 6. Einplanen in Buffer (Organisation „My organization“, Zeitzone Europe/Berlin)
- **TikTok + Instagram:** 16:30 und 23:30 – je ein neuer Teil 1 (oder an einem der Slots ein Teil 2 für einen Gewinner, siehe Teil-1-Strategie).
- **YouTube:** Wunsch des Nutzers = 3 pro Tag (Stadt + Story A + Story B). YouTube lässt über Buffer aber nur **2 Posts je 24 h (gleitend)** zu (mehrfach Fehler „daily posting limit“).
  Solange der Nutzer nicht meldet, dass der Kanal per Telefon verifiziert ist: **Abo-Welt 13:20 + Story A 23:59** (nie 3 Posts in 24 h – vorher die gesendeten YouTube-Posts der letzten 24 h prüfen und notfalls ein paar Minuten später planen).
  Nach Verifizierung: Abo-Welt 10:00, Story A 16:30, Story B 23:30 versuchen; scheitert ein Post am Limit, zurück auf 2 und dem Nutzer melden.
- **Uhrzeiten anpassen:** Die Uhrzeiten richten sich nach den Ergebnissen des `analyse`-Agenten (pipeline/erkenntnisse.md). Empfiehlt er mit genug Daten (mind. 6 Videos je Uhrzeit) eine bessere Uhrzeit, diese direkt übernehmen (Wunsch des Nutzers) und in der Info-Nachricht nennen. YouTube-Limit dabei immer einhalten.
Kanäle: TikTok `6af8aaa962b70b94b030f0a2`, YouTube `6af8a70562b70b94b030ab82`, Instagram `6af8ae8162b70b94b0314c10`.
`create_post` mit `schedulingType: "automatic"`, `mode: "customScheduled"`, `dueAt` (+01:00 Winterzeit / +02:00 Sommerzeit).
- **KEIN KI-Häkchen** (Anweisung des Nutzers vom 17.11.2026): `metadata.tiktok {isAiGenerated: false, title}`, `metadata.youtube {title, categoryId, isAiGenerated: false, madeForKids: false, privacy: "public"}`,
  `metadata.instagram {type: "reel", shouldShareToFeed: true, isAiGenerated: false}`.
- Gratis-Tarif: max. 10 geplante Posts gleichzeitig → vorher `list_posts` (status scheduled) prüfen.
- Texte pro Plattform: TikTok kurz + Frage + 3–5 Themen-Hashtags (KEIN #fyp/#reels); YouTube Titel ≤ 70 Zeichen mit #shorts, Beschreibung mit Frage;
  Instagram Text mit Frage + 3–5 Themen-Hashtags.

## 7. Sonntags-Auswertung
`get_aggregated_post_metrics` / `list_posts` (sent) der letzten 7 Tage: Aufrufe, Likes, Kommentare pro Uhrzeit (16:30 vs. 23:30) und Thema.
Kurze Zusammenfassung an den Nutzer. Nach 3 Wochen (ab 06.12.2026) bessere Uhrzeiten vorschlagen – nur nach „ok“ ändern.

## 8. Technik-Hinweise (20.11.2026)
- Werkzeuge mit `/usr/bin/python3` starten (`python3` im Pfad = /usr/local/bin ohne numpy/faster-whisper).
- Mehrere Videos parallel: OmniVoice mit höchstens 2 Threads je Prozess, sonst bremsen sie sich gegenseitig aus; nie zwei Renders gleichzeitig.
- `tools/piper_flow.py` schreibt Zwischendateien nach `/tmp/s1.wav` usw. → bei Parallelbetrieb in einen Projektordner umleiten.
- **Buffer/YouTube-Limit:** Buffer lässt für YouTube nur **2 geplante Posts pro Tag** zu („maximum number of posts YouTube allows in a day (2)“). Drei YouTube-Videos am Tag gehen so nicht – Nutzer entscheidet, welches Video auf YouTube entfällt.
- **Vermutlich rollierende 24 h (21.11.):** Stadt Tag 1 (19.11. 13:00) und Tag 2 (20.11. 13:00) scheiterten mit „daily posting limit“, weil am Vortag schon 16:30 + 23:30 auf YouTube liefen. Seit 20.11. läuft YouTube nur 13:00 + ca. 23:30 – dann passt es. Nie 16:30 auf YouTube. Den YouTube-Spätpost einige Minuten NACH dem Vortags-Spätpost (+24 h) legen (z. B. 23:45). Nach dem Senden Fehlerstatus prüfen.
