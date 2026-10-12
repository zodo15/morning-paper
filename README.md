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
