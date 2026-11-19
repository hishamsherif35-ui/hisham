# Hisham Sherif Hassan – portfolio site

This is a static one-page site with no build step. Vercel deploys every push to `main` automatically.

## Files
- `index.html` holds the whole site (CSS and JS inline). Content is edited in the arrays at the top of the `<script>`:
  - `CATEGORIES`: each category has a `videos` list of `{ title, ratio: "16:9" | "9:16", src, poster }`. The first video in a list opens first.
  - `CLIENTS`: `[slug, name, width, height]`, shown in the right-hand logo strip in this order (big brands first).
  - `CONTACT`: icon buttons only. Never print the email or phone number as visible text (Hisham asked for that).
- `videos/` holds `<slug>.mp4` and `<slug>.jpg` (poster).
- `logos/` holds dark single-color PNGs (#111214 on transparent).
- `hisham-bg.jpg` is the B&W studio portrait used as the background.

## Adding a video
1. Encode it: `tools/encode-video.sh "<input>" <slug> videos/` uses 2-pass x264 with faststart and also writes the poster jpg. It targets about 13.4 MB because the claude.ai preview artifact caps files at 15 MB. For Vercel only, raise the size target in the script if Hisham wants higher quality. GitHub rejects files over 100 MB.
2. Add `{ title, ratio, src:"videos/<slug>.mp4", poster:"videos/<slug>.jpg" }` to the right category.
3. Commit and push to `main`. The site is live in about a minute.

## Adding a client logo
Convert the logo to the dark monochrome style with `tools/logo-monochrome.py` (see the list at the top of the script: alpha, background-distance or luminance modes). Then add it to `CLIENTS` with its pixel width and height.

## Design rules Hisham set
- Accent color is the REC-dot orange-red `#e5322d`. Use it for numbers, "color grading" and active states.
- Glass buttons and menu with a light sweep on hover. The client strip auto-scrolls even with reduced motion, and its logos are not clickable.
- Intro: an orange playhead types the name in, letter by letter.
- No timeline graphic behind the portrait. It was tried and rejected.
- Categories: Commercial Copies, Events, Documentaries, Social Media Reels, Drone Mapping, AI Copies.
