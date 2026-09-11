#!/usr/bin/env python3
"""Builds website/pack/index.html, the Listing Content Pack page on the agency site.

The page is the prospect-facing surface for the pack: what do I get, what does it cost, when do I
post it. It shows one worked example, 625 North Talbot, with every piece on the page and the six
reels playing inline. Content lives in the lists below so the next listing's page is a data swap.

Assets under website/pack/assets/ are produced from the client pack folder (see the session
summary for the transcode recipe) and are gitignored like the rest of the site's media.

Run: python3 build_pack_page.py
"""
import pathlib, html

HERE = pathlib.Path(__file__).parent
MAIL = "mailto:its.rylexx@gmail.com?subject=Listing%20Content%20Pack%20for%20[your%20address]"

# The six v2 reels (2026-09-10), one format each, in Ryan's order (2026-09-11: his two favourites first).
# (key, name, duration). Keys match pack/assets/reels/<key>.mp4 and posters/<key>.jpg.
REELS = [
    ("V5", "What $1,575,000 gets you", "0:20"),
    ("V4", "Guess the price", "0:18"),
    ("V2", "Two rooms at a time", "0:18"),
    ("V3", "The great room", "0:12"),
    ("V1", "The details", "0:24"),
]
# V6 (fire, water, stone, wood) dropped by Ryan 2026-09-11: "zooming into nothing". Five reels.

# (name, in this pack). Twelve formats; the six marked are the ones this house got.
MENU = [
    ("Two rooms at a time", True),
    ("What $X gets you in [town]", True),
    ("Guess the price", True),
    ("One room, four angles", True),
    ("The details", True),
    ("The film, vertical", False),
    ("Outdoor life", False),
    ("3 things you'd miss in the photos", False),
    ("Coming soon", False),
    ("Open house countdown", False),
    ("Before and after staging", False),
    ("Day to night", False),
]

C1 = [("01_cover", "Cover"), ("02_numbers", "The numbers"), ("03_great_room", "Great room"), ("04_kitchen", "Kitchen"),
      ("05_primary_suite", "Primary suite"), ("06_ensuite", "Ensuite"), ("07_lower_level", "Lower level"),
      ("08_covered_patio", "Covered patio"), ("09_the_backyard", "The backyard"), ("10_cta", "Contact")]
C2 = [("01_cover", "Cover"), ("02_the_water", "The water"), ("03_where_you_sit", "Where you sit"),
      ("04_the_family_end", "The family end"), ("05_from_above", "From above")]
C3 = [("01_cover", "Cover"), ("02_bedroom_1", "Bedroom 1 of 5"), ("03_bedroom_2", "Bedroom 2 of 5"),
      ("04_bedroom_3", "Bedroom 3 of 5"), ("05_bedroom_4", "Bedroom 4 of 5"), ("06_bedroom_5", "Bedroom 5 of 5"),
      ("07_then_downstairs", "Then downstairs"), ("08_rec_room", "Rec room"), ("09_games_room", "Games room"),
      ("10_home_gym", "Home gym")]
# C4 (by day, by dusk) was built 2026-09-11 and dropped the same day: as a static split it made the
# house small and read like an ad. The slides stay in the client folder; the page shows three.

STORIES = [("01_tomorrow", "Drops tomorrow"), ("02_just_listed", "Just listed"), ("03_open_house", "Open house"), ("04_price", "The price")]
CARDS = [("01_coming_soon", "Coming soon"), ("02_just_listed", "Just listed"), ("03_open_house", "Open house"),
         ("04_price_improved", "Price improved"), ("05_sold", "Sold, with the numbers")]

ALBUM = [
    ("01_photo84", "Twilight front, the scroll-stopper. Lit windows read as a home, not a listing."),
    ("02_photo63", "The same house by day, so nobody thinks the twilight shot is hiding something."),
    ("03_photo31", "Straight to the room that sells it. The stone fireplace wall."),
    ("04_photo33", "The kitchen from the angle that gets island, dining and patio doors in one frame."),
    ("05_photo44", "The red dining room, the one room with a colour anyone will remember."),
    ("06_photo27", "The piano room, the second wow. It reads as space, not furniture."),
    ("07_photo4", "Primary bedroom, tray ceiling, ensuite door visible."),
    ("08_photo8", "The ensuite with the soaker tub, because four of the five baths are ensuite."),
    ("09_photo52", "The finished lower level. Most listings stop before this."),
    ("10_photo73", "The covered patio at its best, columns framing the yard."),
    ("11_photo69", "The backyard, with the pool sweeping through the frame."),
    ("12_photo91", "The aerial last. The lot is the thing you cannot get anywhere else in Windsor."),
]

SCHED = [
    ("Day -3", "Coming soon card", "FB + IG"),
    ("Day -1", "Story: drops tomorrow", "Stories"),
    ("Day 0", "Two rooms at a time, Just Listed carousel, Facebook album", "FB + IG"),
    ("Day 2", "What $1,575,000 gets you", "IG reel"),
    ("Day 4", "Guess the price", "IG + FB"),
    ("Day 5", "Story: open house", "Stories"),
    ("Day 7", "The great room", "IG reel"),
    ("Day 8", "The backyard, five ways", "IG carousel"),
    ("Day 10", "The details", "IG + FB"),
    ("Day 11", "The other half", "FB + IG carousel"),
    ("Day 14", "Story: the price", "Stories"),
    ("If it moves", "Price improved card", "FB + IG"),
    ("When it sells", "Sold, with the numbers", "FB + IG"),
]

# (label, Facebook, Instagram). Verbatim from the pack's CAPTIONS.md.
CAPTIONS = [
    ("Two rooms at a time",
     "625 North Talbot Road, two rooms at a time. Five bedrooms, five bathrooms with four of them ensuite, about 5,300 finished square feet including the lower level, on a 100 by 200 foot lot in South Windsor.\n\nStone fireplace in the great room, granite island in the kitchen, in-ground pool and an extra large covered patio out back. Triple garage.\n\n$1,575,000. Message me to see it in person.",
     "Two rooms at a time. 625 North Talbot Road.\n5 bed · 5 bath · 5,300 sq ft · $1,575,000\nDM to see it in person.\n#justlisted #southwindsor #windsorrealestate #yqg"),
    ("What $1,575,000 gets you",
     "This is what $1,575,000 buys in South Windsor right now.\n\nFive bedrooms. Five bathrooms, four of them ensuite. About 5,300 finished square feet with the lower level. A 100 by 200 foot lot with an in-ground pool and an extra large covered patio. Triple garage.\n\n625 North Talbot Road. Message me for a private showing.",
     "What $1,575,000 gets you in South Windsor.\nPool, 100x200 lot, 5 bed, 5 bath.\n625 North Talbot Road.\n#southwindsor #windsorrealestate #yqg #justlisted"),
    ("Guess the price",
     "Five bedrooms, five bathrooms, a pool and a 100 by 200 foot lot in South Windsor. Before the number comes up, what would you guess?\n\nThe answer is at the end. 625 North Talbot Road.",
     "Guess before the end.\n5 bed · 5 bath · pool · 100x200 lot\nSouth Windsor.\n#guesstheprice #windsorrealestate #southwindsor #yqg"),
    ("The great room",
     "One room, four angles, twelve seconds. The great room at 625 North Talbot Road: a stone fireplace wall running floor to ceiling, and the whole main floor opening around it.\n\nFive bedrooms, five bathrooms, about 5,300 finished square feet. $1,575,000.",
     "The best room in the house, in twelve seconds.\n625 North Talbot Road · $1,575,000\n#windsorrealestate #southwindsor #yqg #greatroom"),
    ("The details",
     "The small things at 625 North Talbot Road. The pendants over the granite island, the stone fireplace up close, the chandelier in the ensuite, the piano room, the 625 on the stone out front.\n\nFive bedrooms, five bathrooms, in-ground pool, 100 by 200 foot lot. $1,575,000.",
     "Look closer. 625 North Talbot Road.\n$1,575,000 · South Windsor\n#windsorrealestate #southwindsor #yqg #details"),
    ("Fire, water, stone, wood",
     "The fireplace, the pool, the stone, the hardwood. 625 North Talbot Road, cut by what the house is made of instead of room by room.\n\nFive bedrooms, five bathrooms, about 5,300 finished square feet on a 100 by 200 foot lot in South Windsor. $1,575,000.",
     "Fire, water, stone, wood.\n625 North Talbot Road · $1,575,000\n#southwindsor #windsorrealestate #yqg"),
    ("C1 · Just Listed carousel",
     "Just listed at 625 North Talbot Road, Windsor. $1,575,000.\n\nFive bedrooms. Five bathrooms, four of them ensuite. About 5,300 finished square feet including a finished lower level with a rec room, a gym and a full bath. Brick and stone, triple garage.\n\nOutside, an in-ground pool and an extra large covered patio on a 100 by 200 foot lot.\n\nSwipe through, and message me if you want to see it.",
     "Just listed. 625 North Talbot Road, South Windsor.\n$1,575,000 · 5 bed · 5 bath · 5,300 sq ft · 100x200 lot\nSwipe through. DM to book a showing.\n#justlisted #southwindsor #windsorrealestate #yqg"),
    ("C2 · The backyard, five ways",
     "Five angles on the reason someone will buy this house.\n\nIn-ground pool with a walk-in shallow end and a full safety fence. Extra large covered patio with ceiling fans. Play structure at the back. All of it on a 100 by 200 foot lot.\n\n625 North Talbot Road, $1,575,000.",
     "The backyard, five ways.\nPool, covered patio, playground, 100x200 lot.\n625 North Talbot Road.\n#southwindsor #windsorrealestate #backyardgoals #yqg"),
    ("C3 · The other half",
     "Everyone posts the kitchen. Here is the other half of 625 North Talbot Road.\n\nFive bedrooms, counted out one by one, then the finished lower level: a rec room with a stone fireplace, a games room, a home gym and a full bath. That is where the 5,300 square feet actually is.\n\n$1,575,000. Message me to walk it.",
     "You have seen the kitchen. Here is the rest.\n5 bedrooms, then downstairs.\n625 North Talbot Road · $1,575,000\n#windsorrealestate #southwindsor #yqg"),
    ("C4 · By day, by dusk",
     "The same house, photographed twice. 625 North Talbot Road by day and at dusk, from the same four spots.\n\nBrick and stone, triple garage, on a 100 by 200 foot lot in South Windsor. Five bedrooms, five bathrooms, in-ground pool. $1,575,000.",
     "By day, by dusk. Swipe.\n625 North Talbot Road, South Windsor.\n#southwindsor #windsorrealestate #twilight #yqg"),
    ("Card · Coming soon",
     "Something is coming on North Talbot. Five bedrooms, a pool, and a 100 by 200 foot lot in South Windsor. Photos and the full tour this week.",
     "Coming soon in South Windsor.\n5 bed · pool · 100x200 lot\n#comingsoon #southwindsor #yqg"),
    ("Card · Open house",
     "Open house at 625 North Talbot Road this [day] from [time] to [time].\n\nCome through the whole house, including the finished lower level, and have a look at the backyard. Five bedrooms, five bathrooms, in-ground pool, 100 by 200 foot lot. $1,575,000.\n\nNo appointment needed. Bring whoever you want a second opinion from.",
     "Open house [day], [time].\n625 North Talbot Road, South Windsor.\n#openhouse #southwindsor #windsorrealestate #yqg"),
    ("Card · Price improved",
     "Price improved at 625 North Talbot Road. Now $1,575,000, down from $1,650,000.\n\nSame five bedrooms, same in-ground pool, same 100 by 200 foot lot. If it was close before, it is worth a second look now.",
     "Price improved. Now $1,575,000.\n625 North Talbot Road, South Windsor.\n#pricedrop #southwindsor #windsorrealestate #yqg"),
    ("Card · Sold, with the numbers",
     "Sold. 625 North Talbot Road, South Windsor, in [n] days with [n] offers.\n\nThank you to the sellers for trusting me with it, and congratulations to the buyers.\n\nIf you are thinking about selling in South Windsor and you want to know what your place would do in this market, message me. Happy to give you a straight answer.",
     "Sold in [n] days. [n] offers.\n625 North Talbot Road, South Windsor.\nThinking of selling? DM me.\n#sold #southwindsor #windsorrealestate #yqg"),
    ("The Facebook album",
     "Just listed: 625 North Talbot Road, Windsor. $1,575,000.\n\nFive bedrooms and five bathrooms, four of them ensuite. About 5,300 finished square feet including the lower level, which is finished properly, with a rec room and fireplace, a home gym and another full bath.\n\nThe main floor is built around a stone fireplace wall in the great room, with a granite island kitchen that opens onto it and a separate dining room. Upstairs there are four more bedrooms.\n\nOutside is the part that is hard to find in South Windsor: a 100 by 200 foot lot with an in-ground pool, an extra large covered patio with ceiling fans, and a play structure at the back. Triple garage, brick and stone.\n\nTwelve photos below, in the order I would show you the house.\n\nMessage me to see it in person.",
     "Post the carousel instead. A twelve photo album is a Facebook format, and Instagram caps a carousel at ten anyway."),
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


def album_grid():
    return "".join(
        f'<figure class="shot reveal" style="--d:{(i % 4) * 0.06:.2f}s" data-full="assets/album/{f}.jpg" data-title="Photo {i + 1} of 12" tabindex="0" role="button" aria-label="Open photo {i + 1}">'
        f'<div class="shot-media"><img src="assets/album/{f}.jpg" alt="" width="1600" height="1067" loading="lazy"><span class="shot-no">{i + 1:02d}</span></div>'
        f'</figure>'
        for i, (f, why) in enumerate(ALBUM))


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
<meta name="description" content="One listing, eighteen pieces, two weeks of posts. Five vertical reels, three carousels, a Facebook album, stories, cards, captions and a posting schedule, built from the listing photos in 48 hours.">
<meta property="og:title" content="The Listing Content Pack · Ryan Herbig">
<meta property="og:description" content="One listing, eighteen pieces, two weeks of posts. Built from the listing photos in 48 hours.">
<meta property="og:image" content="https://ryanherbig.vercel.app/pack/assets/album/01_photo84.jpg">
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
    <a href="../#pricing">Pricing</a>
    <a href="../#clients">Testimonials</a>
    <a class="nav-cta" href="{MAIL}">Get a pack</a>
  </nav>
</header>

<main id="top">

<!-- ============================ HERO ============================ -->
<section class="hero pack-hero">
  <div class="container">
    <p class="kicker mask"><span>The Listing Content Pack &middot; $350 &middot; a worked example</span></p>
    <h1 class="hero-title">
      <span class="mask"><span>One listing.</span></span>
      <span class="mask"><span><em>Eighteen pieces.</em></span></span>
      <span class="mask"><span>Two weeks of posts.</span></span>
    </h1>
    <div class="hero-row">
      <p class="hero-sub fade">Everything one listing needs on social for two weeks, made from its photos in 48 hours,
      captions included. This is the pack for 625 North Talbot Road, Windsor.</p>
      <div class="hero-actions fade">
        <a class="btn btn-primary" href="{MAIL}">Get a pack for your listing</a>
        <a class="btn btn-ghost" href="#reels">See the reels</a>
      </div>
    </div>
    <dl class="stats fade">
      <div><dt>Reels</dt><dd><span data-count="5">0</span></dd><span class="stat-sub">12 to 24 seconds, one format each</span></div>
      <div><dt>Carousels</dt><dd><span data-count="3">0</span></dd><span class="stat-sub">25 slides</span></div>
      <div><dt>Album</dt><dd><span data-count="12">0</span></dd><span class="stat-sub">photos, in my order</span></div>
      <div><dt>Stories and cards</dt><dd><span data-count="9">0</span></dd><span class="stat-sub">launch week to sold</span></div>
      <div><dt>Turnaround</dt><dd>48h</dd><span class="stat-sub">from the address</span></div>
    </dl>
  </div>
</section>

<!-- ============================ REELS ============================ -->
<section class="section reels" id="reels">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The reels</p>
      <h2>Five reels. Five different formats.</h2>
      <p class="sec-sub"><span class="hint-hover">Hover to preview, click to watch with sound.</span><span class="hint-touch">Tap one to watch with sound.</span></p>
    </div>
    <div class="phones">{reel_cards()}
    </div>
  </div>
</section>

<!-- ============================ CAROUSELS ============================ -->
<section class="section carousels" id="carousels">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The three carousels</p>
      <h2>Swipe through them here.</h2>
      <p class="sec-sub">Launch day, the feature that sells the house, and the rooms nobody posts. Captions included.</p>
    </div>
    <div class="posts reveal">{carousel("c1", "c1", C1, "Just Listed", "10 slides", CAP["C1 · Just Listed carousel"][1])}{carousel("c2", "c2", C2, "The backyard, five ways", "5 slides", CAP["C2 · The backyard, five ways"][1])}{carousel("c3", "c3", C3, "The other half", "10 slides", CAP["C3 · The other half"][1])}
    </div>
  </div>
</section>

<!-- ============================ STILLS ============================ -->
<section class="section stills" id="stills">
  <div class="container">
    <div class="sec-head sec-head-split reveal">
      <div>
        <p class="eyebrow">Stories and cards</p>
        <h2>Four stories. Five cards.</h2>
        <p class="sec-sub">Stories for launch week. Cards for the whole life of the listing.</p>
      </div>
      <div class="car-nav">
        <button class="car-btn" id="railPrev" aria-label="Scroll back">&#8592;</button>
        <button class="car-btn" id="railNext" aria-label="Scroll forward">&#8594;</button>
      </div>
    </div>
  </div>
  <div class="rail-wrap">
    <div class="rail" id="rail">{rail_items("stories", STORIES, "tall", 1080, 1920)}<span class="rail-gap" aria-hidden="true"></span>{rail_items("cards", CARDS, "wide", 1080, 1350)}
    </div>
  </div>
</section>

<!-- ============================ ALBUM ============================ -->
<section class="section album" id="album">
  <div class="container">
    <div class="sec-head reveal">
      <p class="eyebrow">The Facebook album</p>
      <h2>Twelve photos, one Facebook post.</h2>
      <p class="sec-sub">Plain photos with the written post, in the order you would be shown the house. Instagram gets the carousels, Facebook gets this.</p>
    </div>
    <div class="shots">{album_grid()}
    </div>
  </div>
</section>

<!-- ============================ MENU ============================ -->
<section class="section menu" id="menu">
  <div class="container menu-grid">
    <div class="sec-head reveal">
      <p class="eyebrow">The menu</p>
      <h2>Twelve formats. Your house gets the five that fit.</h2>
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
      <p class="sec-sub">What to post on which day. The card ships in the folder.</p>
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
    </div>
    <div class="plans plans-2">
      <article class="plan is-featured reveal">
        <p class="plan-name">Content pack</p>
        <p class="plan-price">$350</p>
        <p class="plan-terms">From your listing photos</p>
        <p class="plan-desc">Everything on this page, for your listing, back in 48 hours.</p>
        <ul class="plan-list">
          <li>Five vertical reels</li>
          <li>Three carousels and a Facebook album</li>
          <li>Four stories and five cards</li>
          <li>Captions for every piece</li>
          <li>A two-week posting schedule</li>
        </ul>
        <p class="plan-addon">+ $100 and I post it all for you, on the schedule.</p>
        <a class="btn btn-primary" href="{MAIL}">Get a pack</a>
      </article>
      <article class="plan reveal">
        <p class="plan-name">Content pack, from your footage</p>
        <p class="plan-price">$300</p>
        <p class="plan-terms">Already have video and drone clips</p>
        <p class="plan-desc">The same pack, cut from the footage your photographer already shot.</p>
        <ul class="plan-list">
          <li>Everything in the content pack</li>
          <li>Your real footage, nothing generated</li>
          <li>Back in 48 hours</li>
          <li>Same posting add-on</li>
        </ul>
        <a class="btn btn-ghost" href="mailto:its.rylexx@gmail.com?subject=Content%20pack%20from%20my%20footage%20for%20[your%20address]">Send me your footage</a>
      </article>
    </div>
    <p class="plans-note reveal">Just want one vertical reel? $100, any format from the menu above. Want the horizontal listing video? <a href="../video/">That is $150, on its own page.</a></p>
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
