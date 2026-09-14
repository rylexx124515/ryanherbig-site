# ryanherbig.vercel.app — the agency site (v3, clean white)

One-page static portfolio site for the listing video business. No build step, no
framework: `index.html` + `styles.css` + `app.js` + `assets/`.

Design spec: `docs/superpowers/specs/2026-08-30-website-v3-clean-white-design.md`.

## Deploy (Vercel CLI, no git needed)

```sh
cd website
npx vercel --prod
```

Live at **https://ryanherbig.vercel.app** since 2026-09-02 (Vercel project `ryanherbig`,
id `prj_6ngwyS9EDXgBPeAgciImGWjCI0bS`, team `itsrylexx-3107s-projects`). `website/.vercel/`
holds the link and is gitignored by the CLI. The CLI uploads the folder directly, so the
gitignored media ships with it.

First-deploy trap, already fixed: with no `.vercel/` link the CLI created a project named
after the folder (`website`, URL `website-ten-jade-23.vercel.app`) behind Deployment
Protection (302 to a login page). Fixed through the API: PATCH the project with
`{"name":"ryanherbig","ssoProtection":null}`, then POST `ryanherbig.vercel.app` to its
domains. Both URLs now serve the site.

## Local preview

```sh
cd website && python3 -m http.server 8901
# then open http://localhost:8901
```

## Assets (all gitignored, live only on this Mac and on Vercel once deployed)

- `assets/film/*.mp4` — 15 delivered films as 720p web transcodes (~121 MB). The page's
  carousel shows 5 (emerald, talbot, stclair, brady, roselawn); chatham also plays from a
  testimonial link. The rest ship unused, ready to swap in.
- `assets/poster/*.jpg` — matching posters grabbed at 1.5s so each carries that
  client's own title typography.
- `assets/seam/02-photo.jpg` + `02-film.mp4` (720p loop) — the 30 Emerald Lane backyard
  photo-to-film pair shown side by side under "How it works". Chosen for big camera travel.
- `assets/img/hero5.mp4` + `hero5_poster.jpg` — the hero loop since v3.4 (2026-09-02): five 4s
  mid-film camera moves (Talbot twilight, Emerald drone, Brady dining, St. Clair aerial, Roselawn
  backyard), 0.7s crossfades, NO title overlays or end cards, ends on the first 0.7s of clip 1 so
  the loop is seamless. Re-cut 2026-09-02 evening after Ryan saw a stutter on clip 1 and a flash
  at the top of clip 3 (loop repeated 0.7s; Brady window crossed a cut); recipe and window times
  in `scrollcraft/builds/agency-v4/assets/README.md`. 16.5s, 1280x720, 7.0 MB. `hero5-m.mp4` + `hero5-m_poster.jpg` is the same
  cut cropped 4:3 (800x600, 2.7 MB) that phones get instead; the inline script under the video
  picks one at parse time. Master: `scrollcraft/builds/agency-v4/assets/hero-5.mp4`.
- `assets/img/hero_montage.mp4` + `hero_montage_poster.jpg` — the previous hero loop (8 films x 3s
  with room labels baked in, fades through white). Kept on disk, no longer referenced.

Rebuild any of it from the masters in `clients/`. The 15 films and posters were copied
from `scrollcraft/builds/listing-films/assets/`. The montage recipe (ffmpeg xfade chain)
is in the 2026-08-30 session summary.

## Portrait

`#about` is a text-only layout until `assets/img/ryan.jpg` exists. Drop the photo in
(4:5 crops best) and the portrait column appears on its own; no code change.

## v3.4 motion notes (2026-09-02)

- The hero copy is a back plane: `app.js` sets `--hy`/`--ho` on `#heroCopy` so it lags the scroll
  (18%) and dims while the montage frame rises over it. The frame carries a tinted offset shadow
  that dissolves as it goes full bleed, a calm grade (saturate .9) and 6% grain.
- `#about` is `position: sticky; top: 0` and the dark offer + footer sit above it, so the close
  slides up over the About like a curtain. The footer is dark now so the page ends held.
- The dark offer ground is lit (two blue radial washes + 5% grain), not flat ink.
- `.work-sub` carries two hint spans; `(hover: none)` swaps "Hover to preview" for "Tap one to watch".

## Copy rules honored

- The product is a "video" everywhere on the page, never a "film" (Ryan, 2026-09-02; matches the
  cold emails, which say video 45:1). Only asset paths and class names still say film.
- No em or en dashes anywhere in visible copy (§7 #26 — prospect-facing page).
  Check: `grep -nP "[\x{2014}\x{2013}]" index.html` should print nothing.
- Eight testimonial cards (six full quotes plus Kelsey Quick's and Stacey Jones's delivery-day
  lines, same card layout per Ryan), every card with a "Watch the video" link (Rose's goes to her
  Facebook reel, the rest open the player), all verbatim from the clients' own
  Gmail messages (pulled with get_thread / get_message on 2026-09-02, never from a search
  snippet). Rose LaFlamme, Rene Thrasher, Ella Osman, Brandy Robertson: `build_round6.py` /
  `build_round7.py`. Isaac Verge: msg `1a0253520040775d` (2026-08-21, trailing ":)" dropped; the sentence "Thanks Ryan for reaching out and offering me the free first video." cut on 2026-09-02 because the free first video is no longer offered).
  Tim Cummings: thread `1a025901edf4dc1a` (2026-08-21; his "to to" and "dinasour" typos are
  corrected, nothing else touched). Kelsey Quick: thread `19f668ed75f694a9` (2026-08-06,
  "Thank you Ryan! Looks great :) Will definitely keep in touch for future listings", smiley
  dropped). Stacey Jones: thread `19f6651776b23350` (2026-07-18, "yes you did a really great
  job thank you!", leading "Hi Ryan, yes" dropped). Not quoted, on purpose: Pauline Lanoue
  ("Very nice", too thin), Khodr Habib (only a pre-delivery reply, then silence), Gavin Kooner
  (delivered 09-02, no reaction yet), Rob Schussler and Laurie Arruda (never delivered).
- Phone pass (v3.4, then v3.5 on 2026-09-02): under 720px the photo/video pair stacks, the
  eight quotes become a horizontal swipe rail with scroll-snap, hero and offer CTAs go full
  width, the play badge shows on every work card without hover, and the fixed bar pads for
  the notch. v3.5 fixed what an iPhone 14 walk actually showed: the page scrolled 14px
  sideways (the delivered-video figure's slide-in offset poked past the edge before it
  revealed; now `overflow-x:clip` on html/body and the figure slides up on phones), the rail
  left a blank band under short quotes (cards are now equal height with the attribution
  pinned to the bottom, and the type is tiered by length via `q-xs` / `q-s` / `q-l` so a
  five-word quote reads as a pull quote and Tim's 58-word one drops a size), "Watch the
  video" and the footer links were 24px tall (now 44px tap targets), the player did not
  lock scroll on iOS (`body.is-locked` is now `position:fixed` with the scroll offset saved
  and restored, focus restore uses `preventScroll`), and the hero pushed the montage
  entirely below the fold (tightened so the frame peeks in). Also `viewport-fit=cover`
  (without it the safe-area padding was a no-op), `theme-color` white, no grey tap flash.
  Verify with the iPhone 14 descriptor in Playwright webkit: `scrollWidth` must equal 390.
- v3.6 (2026-09-02, after Ryan looked on his actual phone): the hero showed iOS's play glyph
  (Low Power Mode refuses autoplay), the swipe rails hid the testimonials with no cue, and
  every button was a `mailto:` that dumped people into Apple Mail. Now: a poster `<img>` sits
  over the hero video until `playing` fires and playback is retried on the first touch; under
  720px the quotes and the work cards stack vertically (no rails, no marquee; JS skips the
  clone pass on phones) with four quotes up front and a "Show 4 more" button. The mailto buttons were briefly
  replaced by an on-page form with a Vercel relay (`api/ask.js`, commits 574b97a and a9cdefc);
  Ryan preferred the original, so every "Get a video" / "Email me an address" is a `mailto:`
  with the subject prefilled again, and the form and relay are gone.

- Counts (15 videos / 11 realtors) verified against delivered masters 2026-08-24. Bump
  the proof strip, the work headline and the About paragraph together as deliveries land.
- Offer copy matches the round-8 cold email: $150, pay only if you like it, photos
  pulled by me, ~24h turnaround.

## Live on GitHub Pages while Vercel is blocked (2026-09-09)

**https://rylexx124515.github.io/ryanherbig-site/** serves this folder from the public repo
`rylexx124515/ryanherbig-site` (built site plus media, ~200 MB). All links on all three pages are
relative (`video/`, `../pack/`, `../#pricing`) so the same files work under the Pages subfolder
and on Vercel. To update: rebuild the pack page, then
`rsync -a --exclude .vercel --exclude __pycache__ --exclude .gitignore ./ <pages-repo>/` and push.

Pricing shown on the site (2026-09-09): Listing video $150 pay-if-you-like · Content pack $350
from photos, +$100 posted · Content pack from the realtor's own footage $300 · one vertical reel
$100 as a footnote. No $200 film anywhere on the site.

## 2026-09-12: the three-reviewer pass, and ryanherbig.ca

- **Hosting:** https://ryanherbig.ca is the only address. Cloudflare Workers static assets, Git-connected
  to `rylexx124515/ryanherbig-site` (build command empty, deploy `npx wrangler deploy`, config in
  `wrangler.jsonc`, `.assetsignore` keeps scripts and dotfiles out). Every push to that repo deploys in
  about a minute. `workers_dev` and preview URLs are off; GitHub Pages was disabled via the API
  (`gh api -X DELETE repos/rylexx124515/ryanherbig-site/pages`, re-enable with a PUT if ever needed).
  No www record on purpose (Ryan: only the bare domain).
- **Copy and structure** (from three parallel reviews: comprehension, conversion, visual QA): every hero
  leads with price and "you see it before you pay"; the proof band sits above the pricing cards; the
  home has two plans with the $300 from-your-footage pack as a line in the pack card; pack pricing
  comes right after the carousels; three short quotes precede every price; every mailto prefills
  Address / MLS link / Name and brokerage; "cards" are "graphics", "film" is gone; counts are
  **17 videos / 12 realtors, "videos made"** (Riverside and Forest added to the work; Rose LaFlamme's
  Facebook-only video is not counted).
- **CSS:** ghost buttons have a visible border, the carousel fades at its edges, the pack shelf is five
  columns on the page rail, the lone third carousel centres, quotes fold to four on every width with a
  text link, the schedule card is sticky, kickers balance, the phone hero has no shadow block.

## 2026-09-11, evening: five reels, three carousels (Ryan's review)

- Ryan reordered the reels (his two favourites first: what $1,575,000 gets you, guess the price,
  two rooms at a time, the great room, the details) and dropped V6 (fire, water, stone, wood).
  C4 (by day, by dusk) was dropped too. Eighteen pieces. The `.phones` grid is five columns.
- Three re-masters, all $0: V3 lost its 1.6 s opener (a jump cut into the same wall), V1's room
  labels now hold across the clip and its detail still and its closer uses the 5 s twilight
  source, V2's header no longer drops out before the end card. The last one was a toolkit bug:
  `reels/v2/lib.py` now cuts every segment to an exact frame count and snaps persistent overlay
  times onto the real timeline. A cut-time checker lives in the session scratchpad notes.
- Album section renamed "Twelve photos, one Facebook post" with a line saying what it is.

## 2026-09-11: the v2 reels and four carousels (superseded the same evening, see above)

- `/pack/` now shows the six **v2 reels** (`clients/Isaac Verge - 625 North Talbot/pack/reels/v2/`,
  one format each, 12 to 24 s), keyed V1..V6 in `pack/assets/reels/` and `posters/`, listed on the
  page in posting order (V2, V5, V4, V3, V1, V6) with a 01..06 badge instead of the internal key.
  The old F1/F2/S1/S2/S12/S3 transcodes were removed from the site; the masters stay in the client folder.
  Transcode recipe: player copy `scale=720:1280`, x264 CRF 22, AAC 128k 48 kHz, faststart; hover
  preview `scale=540:960`, CRF 26, no audio; poster = frame at 2.0 s, JPEG q3.
- **Four carousels**: C1 Just Listed, C2 the backyard, plus the new **C3 The other half** (the five
  bedrooms counted, then the lower level, 10 slides) and **C4 By day, by dusk** (the same four
  exteriors by day and at dusk, split on one slide, 5 slides). Built in
  `clients/.../pack/carousels/C3_other_half/` and `C4_day_dusk/` on the same `slidekit`, rendered
  with `render.py`, exported here as `pack/assets/c3/` and `c4/` (1080x1350 JPEG q82).
- Hero says twenty pieces (6 + 4 + 1 + 4 + 5); the stat strip is reels / carousels / album /
  stories and cards / turnaround. The schedule (page list and the card image) posts the carousels
  on days 0, 3, 8 and 11. The format menu is twelve plain names, numbered, six marked.
- `pack/build_shelf.py` rebuilds `assets/img/pack-shelf.jpg` (the home page's pack card) from the
  posters in posting order; run it whenever the posters change.
- Home: the pack card and the pricing plan say four carousels; the pricing heading is
  "One price each. Nothing up front."

## Three pages (2026-09-09 evening, Ryan's restructure)

The site sells two things, so it is three pages sharing one nav (Listing video · Content pack ·
Testimonials · About · Get a video) and one `styles.css`:

- `/` the home: who Ryan is, the hero montage, **the two offer cards** (`.offer-cards`, the
  video card hover-previews the Talbot film, the pack card shows `assets/img/pack-shelf.jpg`,
  six reel posters composed with PIL from `pack/assets/posters/`), how it works, testimonials,
  about, and the dark offer block with both prices ($150 video, $350 pack) linking to their pages.
  The photo-to-video pair and the work carousel moved off the home to `/video/`.
- `/video/` the horizontal listing video: hero + a featured Talbot player, four "what you get"
  facts, the photo-to-video pair, the carousel of all fifteen films, the three steps, $150.
- `/pack/` the content pack, below (six v2 reels and four carousels since 2026-09-11, see above).

`app.js` is shared by `/` and `/video/`; every block guards on its elements (no montage on the
video page, no carousel on the home). `/pack/` keeps its own `pack.js`.

## /pack, the Listing Content Pack page (2026-09-09)

`pack/index.html`, served at `/pack`, linked from the home page since the evening restructure
(the earlier `noindex` is gone). It shows one
worked example, 625 North Talbot, with all eighteen pieces on the page: six vertical reels
that hover-preview and open in a portrait player with sound, two swipeable carousels with
their captions, the stories and cards rail, the twelve-photo album with the reason per slot,
the twelve-format menu, the two-week schedule, every caption, and the four-row pricing block
($100 reel, $200 film, $350 pack, $450 pack posted, from the locked pack pricing).

- `pack/build_pack_page.py` writes `pack/index.html`; all copy and piece lists are data at the
  top of the script, so the next listing's page is a data swap. Run it after any edit.
- `pack/pack.css` and `pack/pack.js` sit on top of `styles.css` and reuse its tokens, topbar,
  offer block, player and reveal classes. The home page's `app.js` is not loaded here.
- `pack/assets/` (gitignored, 61 MB): `reels/<key>.mp4` are 720x1280 CRF 22 x264 player copies
  cut from the masters, `reels/<key>_540.mp4` are the 540p hover previews copied from the
  client pack's `reels/_pack/`, `posters/` are frames at 2.0s. `c1/`, `c2/`, `stories/`,
  `cards/`, `schedule/` are the PNG renders as 1080-wide JPEG q82; `album/` is 1600 wide.
  Source: `clients/Isaac Verge - 625 North Talbot/pack/`.
- Dash check covers the three pack files too:
  `grep -nP "[\x{2014}\x{2013}]" pack/index.html pack/pack.css pack/pack.js` prints nothing.
- Verified 2026-09-09 in Playwright at 1440 and 390: zero console errors, `scrollWidth` equals
  the viewport, and every interaction (hover preview, portrait player, carousel arrows, dots,
  keyboard, slide and album lightbox, rail arrows, captions picker) driven and checked.

**Hosting note (2026-09-09):** the whole Vercel Hobby team was soft-blocked on 2026-09-06 for
`FAIR_USE_LIMITS_EXCEEDED` (overage type `edgeRequest`), so every project on the account,
this site included, returns HTTP 402 `DEPLOYMENT_DISABLED`, and `vercel --prod` is refused
with "Your Team exceeded our fair use limits and has been blocked." The pack page is built
and previewable locally but could not be deployed. See the 2026-09-09 session summary.
