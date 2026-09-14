# Cyberia — Website Source

A plain HTML/CSS site (no frameworks, no build tools required to run it) with
one config file for your business details, so you can update your name, phone
number, address and stats in one place instead of hunting through 9 pages.

## Folder structure

```
cyberia-site/
├── site_config.json     ← your business details live here (edit this first)
├── build_site.py        ← run this to regenerate the site after any change
├── style.css             shared stylesheet used by every page
├── images/               drop product/service photos here (see below)
├── templates/            page content — edit headings/text here
│   ├── index.html
│   ├── hardware.html
│   ├── repairs.html
│   ├── security.html
│   ├── software.html
│   ├── mercury.html
│   ├── amc.html
│   ├── about.html
│   └── contact.html
└── build/                generated output — this is what you publish/upload
```

## Editing in VS Code

1. Open the folder in VS Code: **File → Open Folder…**
2. Install the **Live Server** extension (by Ritwick Dey) if you want the
   preview to auto-refresh as you edit — right-click `build/index.html` and
   choose **"Open with Live Server"**.
3. Three things are editable:
   - **`site_config.json`** — business name, phone, email, address, business
     hours, stats, and the map/reviews links. Change a value, save, and
     re-run the build script.
   - **`templates/*.html`** — the actual page copy: headings, paragraphs,
     service descriptions, card text. Edit these directly. Just leave any
     `{{LIKE_THIS}}` marker alone — those get filled in automatically from
     `site_config.json` when you build.
   - **`images/`** — drop a photo in with the right filename and it fills the
     matching card automatically (see below).
4. After any edit, regenerate the live pages:
   ```bash
   python3 build_site.py
   ```
   This reads `templates/*.html` + `site_config.json` + `images/`, and writes
   the final pages into `build/`. Re-run it every time you change any of
   them — `build/` is fully overwritten each time, so never edit files inside
   `build/` by hand.

   To sanity-check your config without writing anything (useful after adding
   a new `{{TOKEN}}` to a template), run:
   ```bash
   python3 build_site.py --check
   ```

## Adding photos to the service cards

The Hardware, Repairs and Security pages each have an image box sized to fit
inside the card. Until you add a real photo, that box shows a dashed
placeholder naming the exact file it's waiting for — so you always know what
to add. Just drop a photo into `images/` using that exact filename (see
`images/README.txt` for the full list) and re-run `python3 build_site.py`.
Roughly a 3:2 landscape photo looks best; the box crops/fills automatically.

## What's already filled in vs. still a placeholder

`site_config.json` now has your real business name, phone numbers, email,
address, hours and stats. One thing still needs attention:
- The **testimonials** on the home page are placeholder quotes — swap in real
  customer quotes, or leave just the "Read Our Reviews on Google" button.

## The contact form (already wired up)

`contact.html` submits to [FormSubmit.co](https://formsubmit.co) — no
account, no API key. It posts straight to whatever `EMAIL` is set to in
`site_config.json` (currently `sales@incyberia.com`).

**One-time activation:** the very first real submission after this site goes
live will make FormSubmit send that inbox an "Activate Form" email — click
the link in it once, and every submission after that arrives automatically.
Nothing else to configure.

**The `_next` redirect** sends visitors to `thank-you.html` after they
submit. It's built from `SITE_URL` in `site_config.json`, currently guessed
as `https://incyberia.com` from your email domain — update that field to
your actual domain once hosting is finalised, then rebuild, or the redirect
will point at the wrong place.

If you outgrow FormSubmit's free tier or want a dashboard of submissions,
Formspree is a drop-in alternative — swap the `action` URL and `_subject`
becomes their own field name, but the rest of the form stays the same.

## Google reviews / testimonials

`GOOGLE_REVIEWS_LINK` in `site_config.json` (currently your Google Maps
listing link) powers the "★ Read Our Reviews on Google" button on the home
page — clicking it takes visitors straight to your reviews on Google.

That's the no-signup option. If you'd rather show actual review cards
pulled live from Google directly on the page (star ratings, reviewer names,
auto-updating), that needs one of:
- A **Google Places API key** (via Google Cloud, has a free tier but needs a
  billing account on file), or
- A **third-party widget** (e.g. Elfsight, EmbedSocial, Trustindex) — free
  tiers exist, you sign up and paste in an embed snippet.

Either requires an account only you can create. Once you have a key or embed
snippet, send it over and it can be wired into the home page.

## Publishing

Once `build/` looks right, upload everything inside `build/` (the `.html`
files, `style.css`, and the `images/` folder) to your web host exactly as
they are — there's nothing further to compile.
