# The Morning Paper

A personal daily newspaper as a static website. No build step, no dependencies:
plain HTML/CSS/JS deployed on Vercel.

## Structure
- `index.html` - shell, hash router target
- `styles.css` - newsprint design system (Fraunces / Source Serif 4 / Inter)
- `app.js` - router (today / archive / edition / longread), audio players with
  playback-speed control, and a reader mode that highlights each word as the
  browser speech voice reads it
- `data/editions.js` - `window.PAPER_DATA`: all editions, long reads, audio map
- `photos/` - title pictures (hero photos + generated plates)
- `fonts/` - variable woff2

## Adding a new edition (daily publish)
1. Append the day's structured edition to `window.PAPER_DATA.editions` in
   `data/editions.js`, add its `meta` entry, bump `PAPER_DATA.today`.
   Put the day's One Concept a Day (single merged section, includes Did You
   Know) on the edition record as `concept: {label, name, line}`. The site
   renders one concept slot on the Today page only; past editions stay as
   published. Section names are never hardcoded - groups render from data.
2. Drop the day's images into `photos/`.
3. When audio exists, set `PAPER_DATA.audio["<day>"] = { full: "audio/<day>-full.mp3", quick: "audio/<day>-quick.mp3" }`
   and commit the mp3s under `audio/`.
4. Commit and push to `main`; Vercel redeploys automatically.

Editions 1-7 (the trial week, Oct 6-12 2026) ship with placeholder audio;
the players unlock from edition 8.

## Daily publish contract (from edition 8, Oct 13 2026)

Every morning, three artifacts move from the newspaper pipeline to this repo:

| What | From | Format |
| --- | --- | --- |
| Edition source | newspaper agent | `editions-src/day-N.json` (schema below) |
| Full-read audio | main (TTS) | any audio file + the full-read script as .txt |
| Quick-listen audio | main (TTS) | any audio file |

Publish steps (publisher: the site task agent):

1. Convert the edition File into `editions-src/day-N.json`. Required:
   `day`, `meta{date,short,longread}`, `edition{fact,intro,groups,concept}`.
   `concept` is the single merged One Concept a Day section
   (`{label:"One concept a day",name,line}`) - the site renders one concept
   slot on the Today page only. Section names are never hardcoded; groups
   render from data. Past editions are immutable.
2. `python3 scripts/publish_day.py editions-src/day-N.json --full FULL.mp3 --quick QUICK.mp3 --script-full full-read-script.txt`
   - validates schema and day sequence
   - converts audio to AAC m4a 64k mono in `audio/`
   - derives sentence-sync timings for the full read from the audio itself
     (silence detection + script alignment) into `audio/dN-full.times.json`
   - regenerates `data/editions.js` (never edit that file by hand)
3. Push the printed file list to GitHub; Vercel auto-deploys in ~1 min.
4. Verify live at 390px: edition page renders, both players play,
   concept card populated, charts present, highlight follows the full read.

Script ground rules for the highlight to stay real:
- The full-read script must follow the printed text section by section, in
  paper order. Spoken glue (greeting, transitions) and numbers spelled as
  words are fine - the aligner normalizes and skips those.
- If the aligner reports <80% block coverage, inspect before publishing;
  blocks that do not match simply get no highlight, never wrong highlight.
- No timestamps are ever invented: sentence times come from the audio's own
  speech/pause structure mapped to the script.
