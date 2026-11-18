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
Es gibt zwei Helfer (Ordner `.claude/agents/` im Zweig `main`, als Subagent über das Agent-Werkzeug aufrufen):
- **`recherche`** – sucht Trend-Themen und prüft alle Fakten mit Quellen. Liefert fertige Daten (Kandidaten, Zahlen, Fakten, Quellen).
- **`video-produktion`** – baut, schneidet, rendert und prüft ein Video aus diesen Daten (Türme oder Stadt).
Der Haupt-Ablauf (du) verteilt die Aufgaben, lädt hoch, plant in Buffer ein und benachrichtigt den Nutzer.

Pro Tag:
- **Türme A** und **Türme B**: zwei Trend-Themen aus ALLEN Bereichen (Geld, Länder, Tiere, Rekorde, Technik, Essen, Promis, Sport, Geschichte, Natur …) – nicht nur Fußball, nie zweimal derselbe Bereich an einem Tag.
  Themen müssen überraschen („Platz 1 hätte keiner gedacht“). Trends kostenlos über WebSearch (Google Trends DE, aktuelle News, was gerade viral ist).
- **Stadt (nur YouTube)**: „Unsere YouTube-Stadt“ – jeden Tag neue Häuser für Leute, die unter YouTube-Videos ihren Hauswunsch kommentieren (Abschnitt 1b).

## 1b. YouTube-Stadt (Zustand in `pipeline/stadt-youtube/stadt.json`)
- Kommentare lesen: vidIQ `vidiq_video_comments` mit channelId `UCHkoA2sBD7_hbxF-4et4LLg`, order "time", maxResult 50 – **höchstens EIN Aufruf pro Tag** (5 Gratis-Credits).
  Vorher `vidiq_balance` (kostenlos) prüfen: unter 5 Credits → KEIN Abruf, nur die offenen Wünsche aus stadt.json verwenden. **Niemals Credits kaufen.**
  Bis 30.11.2026 sind nur noch ~20 Credits übrig → Kommentare nur jeden 2. Tag lesen, ab 01.12. täglich.
- Neue Wünsche seit `kommentare_gelesen_bis` in `wuensche_offen` übernehmen (Name = Handle ohne @, max. 12 Zeichen, Großbuchstaben; ein Haus pro Person; Beleidigungen/Politik ignorieren).
- Pro Tag 4–8 Wünsche bauen (älteste zuerst), in `haeuser` eintragen (mit `tag`), aus `wuensche_offen` entfernen, `tag` +1, `kommentare_gelesen_bis` setzen, Datei committen + pushen (Zweig pipeline).
- Keine offenen Wünsche → Video zeigt die wachsende Stadt + großer Aufruf „Kommentier deinen Namen + Wunschhaus und abonnier – morgen steht dein Haus!“.
- Jedes Stadt-Video endet mit diesem Aufruf (Ziel: YouTube-Abos).

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
Kanäle: TikTok `6af8aaa962b70b94b030f0a2`, YouTube `6af8a70562b70b94b030ab82`, Instagram `6af8ae8162b70b94b0314c10`.
`create_post` mit `schedulingType: "automatic"`, `mode: "customScheduled"`, `dueAt` (+01:00 Winterzeit / +02:00 Sommerzeit).
- **TikTok + Instagram (2 pro Tag):** Türme A um 16:30, Türme B um 23:30.
- **YouTube (3 pro Tag):** Stadt um 13:00, Türme A um 16:30, Türme B um 23:30.
- **KEIN KI-Häkchen** (Anweisung des Nutzers vom 17.11.2026): `metadata.tiktok {isAiGenerated: false, title}`, `metadata.youtube {title, categoryId, isAiGenerated: false, madeForKids: false, privacy: "public"}`,
  `metadata.instagram {type: "reel", shouldShareToFeed: true, isAiGenerated: false}`.
- Gratis-Tarif: max. 10 geplante Posts gleichzeitig → vorher `list_posts` (status scheduled) prüfen.
- Texte pro Plattform: TikTok kurz + Frage + 3–5 Themen-Hashtags (KEIN #fyp/#reels); YouTube Titel ≤ 70 Zeichen mit #shorts, Beschreibung mit Frage;
  Instagram Text mit Frage + 3–5 Themen-Hashtags.

## 7. Sonntags-Auswertung
`get_aggregated_post_metrics` / `list_posts` (sent) der letzten 7 Tage: Aufrufe, Likes, Kommentare pro Uhrzeit (16:30 vs. 23:30) und Thema.
Kurze Zusammenfassung an den Nutzer. Nach 3 Wochen (ab 06.12.2026) bessere Uhrzeiten vorschlagen – nur nach „ok“ ändern.
