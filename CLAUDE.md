# storyfakten-videos – täglicher Video-Ablauf

Dieses Repository ist Werkzeugkasten und Ablage für die automatisch erstellten Kurzvideos des Kanals
**storyfakten.statistiken** (TikTok, YouTube Shorts, Instagram Reels; Sprache Deutsch, junges Publikum).

- Werkzeuge: Zweig `pipeline`, Ordner `pipeline/` (Anleitung: `pipeline/ABLAUF.md`).
- Fertige Videos: Zweig `videos`, Ordner `videos/JJJJ-MM-TT-<thema>.mp4`. Öffentlicher Link für Buffer:
  `https://raw.githubusercontent.com/afghaniozey-star/storyfakten-videos/videos/videos/<datei>.mp4`
- Nie Passwörter oder API-Schlüssel in den Chat, ins Repo oder in Commits schreiben.

## Helfer-Agenten (`.claude/agents/`)
- `analyse`: wertet die Accounts über Buffer aus (Zahlen pro Video, Uhrzeit, Thema) → `pipeline/erkenntnisse.md`.
- `trend-scout`: untersucht Trend-Formate und Video-Gestaltung, bewertet unsere Videos, schlägt Verbesserungen vor.
- `recherche`: findet konkrete Themen und prüft jeden Fakt mit Quellen.
- `video-produktion`: baut, schneidet, vertont, rendert und prüft die Videos.
- `qualitaet`: Endkontrolle jedes Videos vor dem Veröffentlichen → FREIGEGEBEN oder GESPERRT mit Grund.
Der tägliche Ablauf steht in `pipeline/ABLAUF.md` (Zweig `pipeline`).
