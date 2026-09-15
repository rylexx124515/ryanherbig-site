#!/usr/bin/env python3
"""Builds website/pack/index.html, the Listing Content Pack page on the agency site.

The page is the prospect-facing surface for the pack: what do I get, what does it cost, when do I
post it. It shows one worked example, 625 North Talbot, with every piece on the page and the five
reels playing inline. Content lives in the lists below so the next listing's page is a data swap.

Assets under website/pack/assets/ are produced from the client pack folder (see the session
summary for the transcode recipe) and are gitignored like the rest of the site's media.

Run: python3 build_pack_page.py
"""
import pathlib, html

HERE = pathlib.Path(__file__).parent
MAIL = "mailto:its.rylexx@gmail.com?subject=Content%20pack&amp;body=Address%3A%0A%0AMLS%20link%20(if%20you%20have%20one)%3A%0A%0AName%20and%20brokerage%3A%0A"
MAIL300 = "mailto:its.rylexx@gmail.com?subject=Content%20pack%20from%20my%20footage&amp;body=Address%3A%0A%0ALink%20to%20your%20footage%20(Drive%2C%20Dropbox%2C%20anything)%3A%0A%0AName%20and%20brokerage%3A%0A"

# The six v2 reels (2026-09-10), one format each, in Ryan's order (2026-09-11: his two favourites first).
# (key, name, duration). Keys match pack/assets/reels/<key>.mp4 and posters/<key>.jpg.
REELS = [
    ("F1", "The film", "0:24"),
    ("V5", "What $1,499,900 gets you", "0:20"),
    ("V4", "Guess the price", "0:18"),
    ("V2", "Two rooms at a time", "0:18"),
    ("V1", "The details", "0:24"),
]
# 2026-09-14: the vertical film (F1, Isaac-approved 09-03, music swapped to the 110 BPM track) replaces
# the great room reel (V3), which Ryan called "so lame, I just see one room".
# V6 (fire, water, stone, wood) dropped by Ryan 2026-09-11: "zooming into nothing". Five reels.

# (name, in this pack). 2026-09-15: Ryan cut "one room four angles", "outdoor life", "3 things you'd
# miss in the photos" and "day to night". Eight formats; the five marked are the ones this house got.
MENU = [
    ("Two rooms at a time", True),
    ("What the price gets you", True),
    ("Guess the price", True),
    ("The details", True),
    ("The listing video, vertical", True),
    ("Before and after staging", False),
    ("Coming soon", False),
    ("Open house countdown", False),
]

C1 = [("01_cover", "Cover"), ("02_numbers", "The numbers"), ("03_great_room", "Great room"), ("04_chefs_kitchen", "Chef's kitchen"),
      ("05_primary_retreat", "Primary retreat"), ("06_spa-inspired_ensuite", "Spa-inspired ensuite"), ("07_lower-level_living", "Lower-level living"),
      ("08_covered_patio", "Covered patio"), ("09_backyard_oasis", "Backyard oasis"), ("10_cta", "Contact")]
C2 = [("01_cover", "Cover"), ("02_resort-style_living", "Resort-style living"), ("03_covered_patio", "Covered patio"),
      ("04_family-friendly_yard", "Family-friendly yard"), ("05_aerial_backyard_view", "Aerial backyard view")]
C3 = [("01_cover", "Cover"), ("02_bedroom_1", "Bedroom 1 of 5"), ("03_bedroom_2", "Bedroom 2 of 5"),
      ("04_bedroom_3", "Bedroom 3 of 5"), ("05_bedroom_4", "Bedroom 4 of 5"), ("06_bedroom_5", "Bedroom 5 of 5"),
      ("07_then_downstairs", "Then downstairs"), ("08_recreation_room", "Recreation room"), ("09_games_room", "Games room"),
      ("10_home_gym", "Home gym")]
# C4 (by day, by dusk) was built 2026-09-11 and dropped the same day: as a static split it made the
# house small and read like an ad. The slides stay in the client folder; the page shows three.

STORIES = [("01_tomorrow", "Drops tomorrow"), ("02_just_listed", "Just listed"), ("03_open_house", "Open house"), ("04_price", "The price")]
CARDS = [("01_coming_soon", "Coming soon"), ("02_just_listed", "Just listed"), ("03_open_house", "Open house"),
         ("04_price_improved", "Price improved"), ("05_sold", "Sold, with the numbers")]

# The twelve-photo Facebook album was dropped from this page 2026-09-15. Ryan: it is the same thing
# as a slideshow and reading both on one page was confusing. The photos still ship in the folder.

SCHED = [
    ("3 days before", "Coming soon graphic", "FB + IG"),
    ("1 day before", "Story: drops tomorrow", "Stories"),
    ("Listing day", "The film, and the Just Listed slideshow", "FB + IG"),
    ("Day 2", "What $1,499,900 gets you", "IG reel"),
    ("Day 4", "Guess the price", "IG + FB"),
    ("Day 5", "Story: open house", "Stories"),
    ("Day 7", "Two rooms at a time", "IG reel"),
    ("Day 8", "Backyard oasis slideshow", "FB + IG"),
    ("Day 10", "The details", "IG + FB"),
    ("Day 11", "The other half slideshow", "FB + IG"),
    ("Day 14", "Story: the price", "Stories"),
    ("If the price changes", "Price improved graphic", "FB + IG"),
    ("When it sells", "Sold graphic, with the numbers", "FB + IG"),
]

# (label, Facebook, Instagram). Verbatim from the pack's CAPTIONS.md.
# (label, Facebook, Instagram). 2026-09-14: rewritten in Isaac's voice, from his own listing page
# copy ("Introducing this beautiful, custom-designed, and fully finished 2-storey home...").
# Facebook gets the full write-up; Instagram gets the short version with a few local hashtags.
FB_CORE = ("Introducing this beautiful, custom-designed and fully finished 2-storey home on a 100 x 200 foot lot in the heart of South Windsor. "
           "5 bedrooms, 5 bathrooms (4 en-suites) and approx. 5,300 sq ft finished, including the lower level.")
FB_CLOSE = "$1,499,900. Contact Isaac Verge for a private showing: 519-564-0903."
CAPTIONS = [
    ("Two rooms at a time",
     "625 North Talbot Road, Windsor. " + FB_CORE + "\n\nHand-scraped hardwood, a stunning stone fireplace in the great room, a chef-inspired kitchen, and a private resort-style backyard with an in-ground pool and extra-large covered patio. Triple car garage.\n\n" + FB_CLOSE,
     "625 North Talbot Road, South Windsor.\n5 bed | 5 bath | approx. 5,300 sq ft | 100 x 200 ft lot\n$1,499,900. DM for a private showing.\n#JustListed #SouthWindsor #WindsorRealEstate #YQG"),
    ("What $1,499,900 gets you",
     "What $1,499,900 gets you in South Windsor.\n\n" + FB_CORE + " A private resort-style backyard with an in-ground pool and extra-large covered patio, and a triple car garage.\n\n625 North Talbot Road. Contact Isaac Verge for a private showing: 519-564-0903.",
     "What $1,499,900 gets you in South Windsor.\n5 bed | 5 bath | pool | 100 x 200 ft lot\n625 North Talbot Road.\n#SouthWindsor #WindsorRealEstate #YQG"),
    ("Guess the price",
     "Five bedrooms, five bathrooms, an in-ground pool and a 100 x 200 foot lot in the heart of South Windsor. What would you guess?\n\nThe answer is at the end. 625 North Talbot Road. Contact Isaac Verge: 519-564-0903.",
     "Guess the price before the end.\n5 bed | 5 bath | pool | 100 x 200 ft lot\nSouth Windsor.\n#GuessThePrice #SouthWindsor #WindsorRealEstate #YQG"),
    ("The film",
     "JUST LISTED | 625 North Talbot Road, Windsor. Take the full walk through, room by room.\n\n" + FB_CORE + " Hand-scraped hardwood, a stunning stone fireplace in the great room, a chef-inspired kitchen, and a private resort-style backyard with an in-ground pool. Triple car garage.\n\n" + FB_CLOSE,
     "JUST LISTED | 625 North Talbot Road, South Windsor.\nThe full walk through.\n5 bed | 5 bath | approx. 5,300 sq ft | $1,499,900\n#JustListed #SouthWindsor #WindsorRealEstate #YQG"),
    ("The details",
     "The finishes that make 625 North Talbot Road: pendant lighting over the chef's kitchen, the stunning stone fireplace, the spa-inspired ensuite, the elegant flex room, and the stone entry out front.\n\n" + FB_CORE + "\n\n" + FB_CLOSE,
     "The finishes at 625 North Talbot Road.\n$1,499,900 | South Windsor\n#WindsorRealEstate #SouthWindsor #YQG"),
    ("Slideshow · Just Listed",
     "JUST LISTED | 625 North Talbot Road, Windsor\n\n" + FB_CORE + " The main floor features beautiful hand-scraped hardwood floors, a warm and inviting great room with a stone fireplace, a stunning chef-inspired kitchen with premium appliances, and a convenient guest suite.\n\nThe backyard offers a private resort-style oasis with an in-ground pool, extra-large covered patio, and lots of privacy. Triple car garage.\n\n" + FB_CLOSE,
     "JUST LISTED | 625 North Talbot Road, South Windsor\n5 bed | 5 bath | approx. 5,300 sq ft | 100 x 200 ft lot\n$1,499,900. Swipe through, then DM for a private showing.\n#JustListed #SouthWindsor #WindsorRealEstate #YQG"),
    ("Slideshow · Backyard oasis",
     "The backyard at 625 North Talbot Road is a private resort-style oasis: an in-ground pool with a walk-in shallow end, an extra-large covered patio, a family-friendly yard, all on a 100 x 200 foot lot in South Windsor.\n\n" + FB_CLOSE,
     "Your own private resort in South Windsor.\nIn-ground pool | covered patio | 100 x 200 ft lot\n625 North Talbot Road | $1,499,900\n#SouthWindsor #WindsorRealEstate #YQG"),
    ("Slideshow · The other half",
     "Five bedrooms and a fully finished lower level at 625 North Talbot Road, Windsor. A spacious primary suite, four more bedrooms, and downstairs an expansive recreation room, games room and home gym with endless possibilities for entertaining and family time.\n\n" + FB_CLOSE,
     "Five bedrooms, then the finished lower level.\n625 North Talbot Road | $1,499,900\n#WindsorRealEstate #SouthWindsor #YQG"),
    ("Graphic · Coming soon",
     "COMING SOON in South Windsor. Five bedrooms, an in-ground pool, and a 100 x 200 foot lot. Full tour and photos this week.",
     "Coming soon in South Windsor.\n5 bed | pool | 100 x 200 ft lot\n#ComingSoon #SouthWindsor #YQG"),
    ("Graphic · Open house",
     "OPEN HOUSE | 625 North Talbot Road, Windsor | [Day], [time] to [time]\n\nTour the whole home, the fully finished lower level and the resort-style backyard. 5 bedrooms, 5 bathrooms, in-ground pool, 100 x 200 foot lot. $1,499,900.\n\nNo appointment needed. Isaac Verge, 519-564-0903.",
     "Open house [day], [time].\n625 North Talbot Road, South Windsor.\n#OpenHouse #SouthWindsor #WindsorRealEstate #YQG"),
    ("Graphic · Price improved",
     "PRICE IMPROVED | 625 North Talbot Road, Windsor. Now $1,499,900.\n\nFive bedrooms, five bathrooms, a private resort-style backyard with an in-ground pool, on a 100 x 200 foot lot in the heart of South Windsor. Contact Isaac Verge for a private showing: 519-564-0903.",
     "Price improved. Now $1,499,900.\n625 North Talbot Road, South Windsor.\n#PriceImproved #SouthWindsor #WindsorRealEstate #YQG"),
    ("Graphic · Sold",
     "SOLD | 625 North Talbot Road, South Windsor, in [n] days with [n] offers.\n\nThank you to our sellers for trusting the Verge Real Estate Team, and congratulations to the buyers.\n\nThinking of selling in South Windsor? Contact Isaac Verge for a free home evaluation: 519-564-0903.",
     "SOLD in [n] days. [n] offers.\n625 North Talbot Road, South Windsor.\nThinking of selling? DM Isaac.\n#Sold #SouthWindsor #WindsorRealEstate #YQG"),
]

e = html.escape
CAP = {label: (fb, ig) for label, fb, ig in CAPTIONS}


def reel_cards():
    out = []
    for i, (k, name, dur) in enumerate(REELS):
        out.append(f'''
      <article class="phone reveal" style="--d:{i * 0.07:.2f}s" data-video="assets/reels/{k}.mp4" data-portrait="1" data-title="{e(name)}" tabindex="0" role="button" aria-label="Play {e(name)}">
        <div class="phone-screen">
          <img src="assets/posters/{k}.jpg" alt="" width="720" height="1280" loading="lazy">
          <video muted playsinline loop preload="none" data-src="assets/reels/{k}_540.mp4"></video>
          <span class="phone-key">{i + 1:02d}</span>
          <span class="phone-dur">{dur}</span>
        </div>
        <div class="phone-meta">
          <h3>{e(name)}</h3>
        </div>
      </article>''')
    return "".join(out)


def carousel(cid, folder, slides, title, sub, caption):
    imgs = "".join(
        f'<li class="slide" data-full="assets/{folder}/{f}.jpg" data-title="{e(title)} · {e(lbl)}">'
        f'<img src="assets/{folder}/{f}.jpg" alt="{e(lbl)}" width="1080" height="1350" loading="lazy" draggable="false"></li>'
        for f, lbl in slides)
    dots = "".join(f'<button type="button" aria-label="Slide {i + 1}"{" class=is-on" if i == 0 else ""}></button>' for i in range(len(slides)))
    return f'''
      <article class="post" id="{cid}">
        <div class="post-head">
          <div><h3>{e(title)}</h3><p>{e(sub)}</p></div>
          <span class="post-count"><b>1</b> / {len(slides)}</span>
        </div>
        <div class="post-stage">
          <ul class="slides">{imgs}</ul>
          <button class="slide-btn slide-prev" type="button" aria-label="Previous slide">&#8592;</button>
          <button class="slide-btn slide-next" type="button" aria-label="Next slide">&#8594;</button>
        </div>
        <div class="post-dots">{dots}</div>
        <p class="post-cap">{e(caption).replace(chr(10), "<br>")}</p>
      </article>'''


def rail_items(folder, items, ratio, w, h):
    return "".join(
        f'<figure class="still still-{ratio} reveal" style="--d:{i * 0.05:.2f}s" data-full="assets/{folder}/{f}.jpg" data-title="{e(lbl)}" tabindex="0" role="button" aria-label="Open {e(lbl)}">'
        f'<div class="still-media"><img src="assets/{folder}/{f}.jpg" alt="" width="{w}" height="{h}" loading="lazy"></div>'
        f'<figcaption>{e(lbl)}</figcaption></figure>'
        for i, (f, lbl) in enumerate(items))


def menu_rows():
    return "".join(
        f'<li class="menu-row{" is-on" if on else ""}"><span class="menu-key">{i + 1:02d}</span><span class="menu-name">{e(name)}</span>'
        f'<span class="menu-tag">{"In this pack" if on else ""}</span></li>'
        for i, (name, on) in enumerate(MENU))


def sched_rows():
    return "".join(
        f'<li class="when-row reveal" style="--d:{i * 0.04:.2f}s"><span class="when-day">{e(d)}</span><span class="when-piece">{e(p)}</span><span class="when-ch">{e(ch)}</span></li>'
        for i, (d, p, ch) in enumerate(SCHED))


def caption_ui():
    picks = "".join(
        f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}"{" class=is-on" if i == 0 else ""}>{e(lbl)}</button>'
        for i, (lbl, fb, ig) in enumerate(CAPTIONS))
    panels = "".join(
        f'<div class="cap-pair" data-i="{i}"{"" if i == 0 else " hidden"}>'
        f'<div class="cap"><span class="cap-net">Facebook</span><p>{e(fb).replace(chr(10), "<br>")}</p></div>'
        f'<div class="cap"><span class="cap-net">Instagram</span><p>{e(ig).replace(chr(10), "<br>")}</p></div></div>'
        for i, (lbl, fb, ig) in enumerate(CAPTIONS))
    return picks, panels


picks, panels = caption_ui()

PAGE = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#FFFFFF">
<title>The Listing Content Pack · Ryan Herbig</title>
<meta name="description" content="One listing, seventeen pieces, two weeks of posts. Five reels built by AI from your listing photos, three slideshows for Instagram and Facebook, four stories, five graphics, a caption for each one in your voice, and a posting schedule. $350, or $250 from footage you already have.">
<meta property="og:title" content="The Listing Content Pack · Ryan Herbig">
<meta property="og:description" content="One listing, seventeen pieces, two weeks of posts. Built from the listing photos in 48 hours.">
<meta property="og:image" content="https://ryanherbig.ca/pack/assets/c1/01_cover.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="pack.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%231B44E4'/><text x='50' y='70' font-size='58' font-weight='800' text-anchor='middle' fill='white' font-family='Arial'>R</text></svg>">
</head>
<body class="pack-page">

<header class="topbar" id="topbar">
  <a class="brand" href="../">Ryan Herbig<span class="brand-sub">Listing Videos</span></a>
  <nav class="topnav">
    <a href="../video/">Listing video</a>
    <a href="./" aria-current="page">Content pack</a>
    <a href="../video/#work">Work</a>
    <a class="nav-pricing" href="#pricing">Pricing</a>
    <a href="../#clients">Testimonials</a>
    <a class="nav-cta" href="{MAIL}">Get a pack</a>
  </nav>
</header>

<main id="top">

<!-- ============================ PAGE HEAD ============================ -->
<section class="hero pack-hero">
  <div class="container">
    <p class="kicker mask"><span>The content pack &middot; $350 &middot; nothing up front</span></p>
    <h1 class="hero-title">
      <span class="mask"><span>One listing,</span></span>
      <span class="mask"><span><em>two weeks of posts.</em></span></span>
    </h1>
    <div class="hero-row">
      <p class="hero-sub fade">Seventeen pieces for one listing, all made from the photos already on it, with
      a written caption for every post and a schedule for putting them out. Everything below is the real pack
      for 625 North Talbot Road in Windsor. Yours is back in 48 hours and you see it before you pay.</p>
      <div class="hero-actions fade">
        <a class="btn btn-primary" href="{MAIL}">Get a pack for your listing</a>
        <a class="btn btn-ghost" href="#reels">See the reels</a>
      </div>
    </div>
    <dl class="stats fade">
      <div><dt>Reels</dt><dd><span data-count="5">0</span></dd><span class="stat-sub">18 to 24 seconds each</span></div>
      <div><dt>Slideshows</dt><dd><span data-count="3">0</span></dd><span class="stat-sub">25 slides, IG and FB</span></div>
      <div><dt>Stories and graphics</dt><dd><span data-count="9">0</span></dd><span class="stat-sub">coming soon to sold</span></div>
      <div><dt>Captions written</dt><dd><span data-count="12">0</span></dd><span class="stat-sub">one per post, in your voice</span></div>
      <div><dt>Turnaround</dt><dd>48h</dd><span class="stat-sub">from the address</span></div>
    </dl>
  </div>
</section>

<!-- ============================ JUMP BAR ============================ -->
<nav class="packnav" aria-label="Jump to a part of the pack">
  <div class="container packnav-row" id="packnav">
    <a href="#reels">Reels</a>
    <a href="#how">How it's made</a>
    <a href="#slideshows">Slideshows</a>
    <a href="#stills">Stories and graphics</a>
    <a href="#branding">Your branding</a>
    <a href="#menu">Formats</a>
    <a href="#schedule">Schedule</a>
    <a href="#pricing">Pricing</a>
  </div>
</nav>

<!-- ============================ REELS ============================ -->
<section class="section reels" id="reels">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The reels</p>
      <h2>Five reels. Five different formats.</h2>
      <p class="sec-sub">No two are built the same way, so a fortnight of posts never feels like the same video
      five times. <span class="hint-hover">Hover to preview, click to watch with sound.</span><span class="hint-touch">Tap one to watch with sound.</span></p>
    </div>
    <div class="phones">{reel_cards()}
    </div>
  </div>
</section>

<!-- ============================ HOW IT IS MADE ============================ -->
<section class="section how-made" id="how">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">How it's made</p>
      <h2>Your photos don't move. These do.</h2>
    </div>
    <div class="made-grid">
      <div class="made-item reveal">
        <h3>The clips are generated, not filmed</h3>
        <p>A listing photo is a still image. AI turns it into a moving shot, so the photo of the kitchen becomes
        a slow push across the kitchen, and five or ten of those cut together into a reel. That is the part you
        are paying for. It is also why there is no camera, no shoot and no day of anyone's time, and why I only
        need the address.</p>
      </div>
      <div class="made-item reveal">
        <h3>The words are copied off you</h3>
        <p>Before anything gets written I read your last posts and your listing write-ups. The captions and the
        text on screen are then written to match how you already sound, so the pack goes out reading like you
        wrote it rather than like a robot did. You get every caption as text, ready to paste.</p>
      </div>
    </div>
    <div class="caps reveal">
      <div class="caps-head">
        <p class="eyebrow">The real captions from this pack</p>
        <p class="caps-sub">Isaac's own listing write-up went in. Pick a piece and read what came back, for
        both networks.</p>
      </div>
      <div class="caps-body">
        <div class="cap-picks" role="tablist" aria-label="Pick a piece">{picks}
        </div>
        <div class="cap-panels">{panels}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================ SLIDESHOWS ============================ -->
<section class="section carousels" id="slideshows">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The slideshows</p>
      <h2>Swipe through them here.</h2>
      <p class="sec-sub">One swipeable post each, and each one goes up on both Instagram and Facebook. Launch
      day, the feature that sells the house, and the rooms nobody posts.</p>
    </div>
    <div class="posts reveal">{carousel("c1", "c1", C1, "Just Listed", "10 slides", CAP["Slideshow · Just Listed"][1])}{carousel("c2", "c2", C2, "Backyard oasis", "5 slides", CAP["Slideshow · Backyard oasis"][1])}{carousel("c3", "c3", C3, "The other half", "10 slides", CAP["Slideshow · The other half"][1])}
    </div>
  </div>
</section>

<!-- ============================ STORIES AND GRAPHICS ============================ -->
<section class="section stills" id="stills">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">Stories and graphics</p>
      <h2>Nine stills. The difference is how long they live.</h2>
      <p class="sec-sub">A <b>story</b> fills the whole phone screen and disappears after 24 hours, so it carries
      the day to day: it drops tomorrow, it's listed, there's an open house. A <b>graphic</b> is a normal post
      that stays on your feed for good, so there's one for every stage the listing goes through. Graphics get
      a written caption, stories don't need one.</p>
    </div>
    <p class="rail-label reveal">Four stories, one a day around the launch</p>
    <div class="rail rail-inline">{rail_items("stories", STORIES, "tall", 1080, 1920)}
    </div>
    <p class="rail-label rail-label-2 reveal">Five graphics, one for each stage</p>
    <div class="rail rail-inline">{rail_items("cards", CARDS, "wide", 1080, 1350)}
    </div>
  </div>
</section>

<!-- ============================ BRANDING ============================ -->
<section class="section brand" id="branding">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">Your branding</p>
      <h2>Same brand. Cleaner.</h2>
      <p class="sec-sub">On the left, the team's own Just Listed template from an earlier listing. Then the same
      announcement as the pack makes it, in three places it has to work. Same logo, same red, same brokerage.</p>
    </div>
    <div class="brand-set reveal">
      <figure class="brand-side is-before" data-full="assets/brand/before.jpg" data-title="Their own template" tabindex="0" role="button" aria-label="Open their own template">
        <img src="assets/brand/before.jpg" alt="The team's own Just Listed template" width="1000" height="1000" loading="lazy">
        <figcaption>Their template</figcaption>
      </figure>
      <figure class="brand-side" data-full="assets/c1/01_cover.jpg" data-title="The pack: the slideshow cover" tabindex="0" role="button" aria-label="Open the slideshow cover">
        <img src="assets/c1/01_cover.jpg" alt="The pack's Just Listed slideshow cover" width="1080" height="1350" loading="lazy">
        <figcaption>The slideshow cover</figcaption>
      </figure>
      <figure class="brand-side" data-full="assets/cards/02_just_listed.jpg" data-title="The pack: the feed graphic" tabindex="0" role="button" aria-label="Open the feed graphic">
        <img src="assets/cards/02_just_listed.jpg" alt="The pack's Just Listed feed graphic" width="1080" height="1350" loading="lazy">
        <figcaption>The feed graphic</figcaption>
      </figure>
      <figure class="brand-side" data-full="assets/stories/02_just_listed.jpg" data-title="The pack: the story" tabindex="0" role="button" aria-label="Open the story">
        <img src="assets/stories/02_just_listed.jpg" alt="The pack's Just Listed story" width="1080" height="1920" loading="lazy">
        <figcaption>The story</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- ============================ MENU ============================ -->
<section class="section menu" id="menu">
  <div class="container menu-grid">
    <div class="sec-head reveal">
      <p class="eyebrow">The menu</p>
      <h2>Eight formats. Your house gets the five that fit.</h2>
      <p class="sec-sub">Picked for the house, not filled in from a template.</p>
    </div>
    <ul class="menu-list reveal">{menu_rows()}
    </ul>
  </div>
</section>

<!-- ============================ SCHEDULE ============================ -->
<section class="section when" id="schedule">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The plan</p>
      <h2>Two weeks, already planned.</h2>
      <p class="sec-sub">What to post on which day, and where. The card ships in the folder.</p>
    </div>
    <div class="when-grid">
      <figure class="when-card reveal" data-full="assets/schedule/schedule.jpg" data-title="The schedule card" tabindex="0" role="button" aria-label="Open the schedule card">
        <img src="assets/schedule/schedule.jpg" alt="The two-week schedule card" width="1080" height="1350" loading="lazy">
      </figure>
      <ol class="when-list">{sched_rows()}
      </ol>
    </div>
  </div>
</section>

<!-- ============================ PRICING ============================ -->
<section class="section pricing" id="pricing">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">Pricing</p>
      <h2>One pack. Two ways to make it.</h2>
      <p class="sec-sub">The difference is where the moving pictures come from. If I have to make them, it's
      $350. If you already paid someone to shoot them, it's $250.</p>
    </div>
    <div class="plans plans-2">
      <article class="plan is-featured reveal">
        <p class="plan-flag">Most listings</p>
        <p class="plan-name">Made from your listing photos</p>
        <p class="plan-price">$350</p>
        <p class="plan-terms">AI builds the moving clips from your stills</p>
        <p class="plan-desc">You have photos and nothing else. Send the address and everything on this page gets
        made from them.</p>
        <ul class="plan-list">
          <li>Five reels, generated from the still photos</li>
          <li>Three slideshows for Instagram and Facebook</li>
          <li>Four stories and five feed graphics</li>
          <li>A caption for every post, written in your voice</li>
          <li>The two-week schedule card</li>
          <li>Back in 48 hours, nothing up front</li>
        </ul>
        <a class="btn btn-primary" href="{MAIL}">Get the $350 pack</a>
        <span class="mail-line">or write to its.rylexx@gmail.com</span>
      </article>
      <article class="plan reveal">
        <p class="plan-name">Made from footage you already have</p>
        <p class="plan-price">$250</p>
        <p class="plan-terms">Your photographer already shot the video</p>
        <p class="plan-desc">You have drone or walk through clips already. Nothing needs generating, so I cut
        yours into the same pieces and it's $100 less.</p>
        <ul class="plan-list">
          <li>The same seventeen pieces, cut from your clips</li>
          <li>Same captions, same graphics, same schedule</li>
          <li>Send a link to the footage, anywhere it lives</li>
          <li>Back in 48 hours, nothing up front</li>
        </ul>
        <a class="btn btn-ghost" href="{MAIL300}">Get the $250 pack</a>
      </article>
    </div>
    <p class="plans-note reveal">Just want one vertical video? $100, any format from <a href="#menu">the menu above</a>.
    Want the horizontal listing video for MLS? <a href="../video/">$150 for thirty seconds, $200 for a minute.</a></p>
  </div>
</section>

<!-- ============================ CLOSE ============================ -->
<section class="section offer" id="get">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">Get started</p>
      <h2>Send me an address.</h2>
      <p class="sec-sub">I pull the photos myself. The pack is back in 48 hours, you look at every piece, and
      then you decide.</p>
    </div>
    <div class="offer-cta reveal">
      <a class="btn btn-primary btn-lg" href="{MAIL}">Email me your listing address</a>
      <span class="offer-mail">its.rylexx@gmail.com</span>
    </div>
  </div>
</section>

</main>

<footer class="footer">
  <div class="container footer-row">
    <span>&copy; 2026 Ryan Herbig &middot; LaSalle, Ontario</span>
    <a href="../">Back to the main site</a>
    <a href="mailto:its.rylexx@gmail.com">its.rylexx@gmail.com</a>
  </div>
</footer>

<!-- ============================ PLAYER / LIGHTBOX ============================ -->
<div class="player" id="player" aria-hidden="true" role="dialog" aria-label="Viewer">
  <button class="player-close" id="playerClose" aria-label="Close">Close</button>
  <div class="player-stage" id="playerStage">
    <video id="playerVideo" controls playsinline preload="none" hidden></video>
    <img id="playerImg" alt="" hidden>
    <p class="player-title" id="playerTitle"></p>
  </div>
</div>

<script src="pack.js"></script>
</body>
</html>
'''

out = HERE / "index.html"
out.write_text(PAGE)
bad = [c for c in PAGE if c in "—–"]
print("wrote", out, len(PAGE) // 1024, "KB", "dashes:", len(bad))
