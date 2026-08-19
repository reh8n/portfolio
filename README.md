# rehan-ali-labs.org

Personal portfolio. One self-contained `index.html` — no build step, no dependencies, no framework.

| File | What it is |
| --- | --- |
| `index.html` | The whole site: markup, styles, and scroll behaviour in one file |
| `og.png` | 1200×630 link-preview image for LinkedIn, WhatsApp, iMessage |
| `netlify.toml` | Security headers, caching rules, `/index.html` → `/` redirect |
| `robots.txt` | Allows all crawlers |

## Deploying

Netlify is connected to this repo. **Any push to `main` deploys automatically** — usually live within a minute. There is nothing to build and nothing to drag.

```bash
git add -A
git commit -m "Add <project name>"
git push
```

## Adding a project

Every project is one `<a class="project-card rise">` block inside `<section class="section-projects">`. Copy the nearest existing card and change four things:

1. **`href`** on the opening `<a>` — where the card links to. If there is no link yet, use `<article class="project-card rise">` … `</article>` instead and the card renders unclickable.
2. **`<h3 class="text-projectcard-title">`** — the project name.
3. **`<p class="text-projectcard-description">`** — the `<span class="text-projectcard-description-company">` holds the role and year; the rest is one or two sentences.
4. **`<div class="mock">`** — the illustration inside the card. Reuse a `.panel` layout from another card and swap the numbers.

Then give the card its own colour wash. In the CSS, near the other `.c-*` rules, add:

```css
.c-yourproject { background:
    radial-gradient(circle at 50% 0, rgba(R,G,B,.22), transparent 70%); }
```

and reference it as `<div class="project-card-colour c-yourproject"></div>`.

Cards are a fixed 588px tall on desktop and grow to fit on mobile, so keep the mock compact — roughly five rows of content is the ceiling.

## Design notes

The visual language is deliberately dark-only: `#101010` ground, `#F2F2F2` text, `#3D3D3D` card borders, cards on `linear-gradient(190deg, #252525, #101010)`. Do not add a light theme — the design is committed to one world.

Type is Neue Montreal with a Gloock italic accent, falling back to Helvetica Neue and Georgia Italic where those are not installed.

## Regenerating the share image

`og.png` is produced by a Pillow script using macOS system fonts (`HelveticaNeue.ttc`, index 10 = Medium upright). Regenerate it whenever the name or headline changes, otherwise link previews go stale.
