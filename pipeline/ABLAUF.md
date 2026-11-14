# Täglicher Ablauf (gestartet um 14:00 Berlin)

## 0. Einrichtung in einer frischen Sitzung
```bash
bash pipeline/setup.sh          # nur nötig, wenn das Setup-Skript der Umgebung es nicht schon erledigt hat
```
Danach gibt es: `/opt/omni/venv` (OmniVoice), `piper`, `faster-whisper`, `ffmpeg`, `npx hyperframes`.

## 1. Themen (2 Videos)
Themen gemischt: Fakten, Statistiken, Storys, Geld & Business, Fußball. Pro Tag zwei verschiedene Bereiche.
Ein Countdown-Format muss passen (Rangliste mit 5–8 Kandidaten und klarer Zahl pro Kandidat).
Jeden Fakt per WebSearch prüfen (mindestens 1 seriöse Quelle pro Zahl), Quellen in der Push-Vorschau nennen.
Keine Themen, die schon in `videos/` liegen (Dateinamen ansehen).

## 2. STIL-REGELN (gelten für JEDES Video – vom Nutzer festgelegt)
1. **Hook in den ersten 2 Sekunden:** überraschende Frage/Behauptung („99 % tippen hier falsch!“) – nicht direkt mit der Liste.
2. **Spannung:** Countdown von hinten nach vorne. Kurze Zwischenfragen („Na, wer fehlt noch?“, „Jetzt wird's eng …“). Gewinner erst ganz am Ende.
3. **Zu jedem Kandidaten ein kurzer, interessanter Fakt** (letzter Titel, berühmtes Ereignis …), nicht nur Name und Zahl.
4. **Tempo:** schnelle Schnitte, kurze Pause vor den großen Momenten. Zahlen & Namen groß, Zoom-Effekte, Soundeffekt bei jedem Platz.
5. **Musik:** lizenzfrei, selbst erzeugt (`tools/musik.py`), leiser als die Stimme, Steigerung zum Finale.
6. **Ende:** Auflösung mit Wow-Effekt (Blitz, Strahlen, Krone, Konfetti, Vergleich) + Frage an die Zuschauer zum Kommentieren.
Länge 35–45 s. Keine fremde Musik, keine fremden Clips/Logos/Wappen (Vereine nur über Farben).

## 3. Video bauen
```bash
cp -r pipeline/vorlage-countdown ~/v/<thema> && cd ~/v/<thema>
# countdown.json + voice.json anpassen (siehe Vorlage: Szenen h1, r<rang>, q1, q2, c1)
/opt/omni/venv/bin/python ~/storyfakten-videos/pipeline/stimme-omni/omni_synth.py .   # Stimme omni-mann, ~1 min/Szene
python3 tools/piper_flow.py .        # Wortzeiten
python3 tools/countdown.py           # Grafik + Musik + Ton
npx -y hyperframes@0.8.228 render -o roh.mp4
ffmpeg -y -i roh.mp4 -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -af "alimiter=limit=0.5:level=false,loudnorm=I=-15:TP=-2:LRA=11,volume=-1dB" -c:a aac -b:a 192k -movflags +faststart final.mp4
```
- voice.json: `groups` = [Anzeige, gesprochen], Zahlen gesprochen ausschreiben. Kurze Einzelwörter mit Kontext („Der FC Barcelona“).
- `wertwort` in countdown.json = das gesprochene Zahlwort genau wie in voice.json; `namewort` für Platz 1.
- Prüfen: Whisper-Abschrift gegen Text, 4–6 Standbilder (`npx hyperframes snapshot`), keine Überlappungen.

## 4. Ablage
Zweig `videos`: `videos/JJJJ-MM-TT-<thema>.mp4` committen und pushen. Link siehe CLAUDE.md.

## 5. Vorschau & Freigabe
Push-Nachricht an den Nutzer (PushNotification-Tool bzw. Abschlussnachricht der Sitzung) mit: Thema, Hook-Satz, Länge,
Quellen, Links zu beiden Videos und den Texten. **Erst nach „ok“ des Nutzers einplanen.**
Kommt das ok zu spät für 16:30, den nächsten freien Termin nehmen (nie in der Vergangenheit).

## 6. Einplanen in Buffer (Organisation „My organization“, Zeitzone Europe/Berlin)
Kanäle: TikTok `6af8aaa962b70b94b030f0a2`, YouTube `6af8a70562b70b94b030ab82`, Instagram `6af8ae8162b70b94b0314c10`.
`create_post` mit `schedulingType: "automatic"`, `mode: "customScheduled"`, `dueAt` (+01:00 Winterzeit / +02:00 Sommerzeit).
- Video 1 → 16:30, Video 2 → 23:30.
- **TikTok bis einschließlich 28.11.2026 nur Video 1 (16:30)**, ab 29.11.2026 beide. YouTube & Instagram immer beide.
- Immer KI-Kennzeichnung: `metadata.tiktok.isAiGenerated: true` (+ `title`), `metadata.youtube {title, categoryId, isAiGenerated: true, madeForKids: false, privacy: "public"}`,
  `metadata.instagram {type: "reel", shouldShareToFeed: true, isAiGenerated: true}`.
- Gratis-Tarif: max. 10 geplante Posts gleichzeitig → vorher `list_posts` (status scheduled) prüfen.
- Texte pro Plattform: TikTok kurz + Frage + 3–5 Themen-Hashtags (KEIN #fyp/#reels); YouTube Titel ≤ 70 Zeichen mit #shorts, Beschreibung mit Frage;
  Instagram Text mit Frage + 3–5 Themen-Hashtags.

## 7. Sonntags-Auswertung
`get_aggregated_post_metrics` / `list_posts` (sent) der letzten 7 Tage: Aufrufe, Likes, Kommentare pro Uhrzeit (16:30 vs. 23:30) und Thema.
Kurze Zusammenfassung an den Nutzer. Nach 3 Wochen (ab 06.12.2026) bessere Uhrzeiten vorschlagen – nur nach „ok“ ändern.
