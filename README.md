# rehan-ali-labs.org

Personal portfolio. Self-contained HTML pages: no build step, no dependencies, no framework.

| File | What it is |
| --- | --- |
| `index.html` | The home page: hero, project cards, experience, footer |
| `prospector.html` | Case study page for Prospector |
| `tools/build-artifact.py` | Builds a single-file copy for publishing as a Claude Artifact |
| `img/` | Project screenshots, served as WebP |
| `og.png` | 1200×630 link-preview image for LinkedIn, WhatsApp, iMessage |
| `netlify.toml` | Security headers, caching rules, `/index.html` → `/` redirect |
| `robots.txt` | Allows all crawlers |

## Deploying

Netlify is connected to this repo. **Any push to `main` deploys automatically**, usually live within a minute. There is nothing to build and nothing to drag.

```bash
git add -A
git commit -m "Add <project name>"
git push
```

## Adding a project

Every project is one `<a class="project-card rise">` block inside `<section class="section-projects">`. Copy the nearest existing card and change four things:

1. **`href`** on the opening `<a>`, where the card links to. If there is no link yet, use `<article class="project-card rise">` … `</article>` instead and the card renders unclickable.
2. **`<h3 class="text-projectcard-title">`** is the project name.
3. **`<p class="text-projectcard-description">`** holds the role and year in `<span class="text-projectcard-description-company">`; the rest is one or two sentences.
4. **`<div class="mock">`** is the illustration inside the card. Reuse a `.panel` layout from another card and swap the numbers, or use a `.shots` carousel of real screenshots as SaveMyPrinter does.

Then give the card its own colour wash. In the CSS, near the other `.c-*` rules, add:

```css
.c-yourproject { background:
    radial-gradient(circle at 50% 0, rgba(R,G,B,.22), transparent 70%); }
```

and reference it as `<div class="project-card-colour c-yourproject"></div>`.

Cards are a fixed 588px tall on desktop and grow to fit on mobile, so keep the mock compact: roughly five rows of content is the ceiling.

## Publishing a preview

An artifact publish carries exactly one HTML file, so relative images and page links break in it. Rebuild the single-file copy first:

```bash
python3 tools/build-artifact.py
```

It writes `dist/artifact.html` with every image inlined as a data URI, `loading="lazy"` stripped (pointless once the bytes are in the document, and some renderers never fire it), and internal page links repointed at the live site. Production files are untouched. Re-run it after changing any image or adding a page.

`dist/` is ignored by git; it is a build output, not source.

## Case study pages

A project with more to say than a card gets its own page, `<project>.html`, linked from its card. `prospector.html` is the pattern: hero with tagline, tech pills and a repo button, then problem, build, numbered steps, decision cards, testing, a captioned gallery and a closing call to action.

Each page repeats the token block and the shared components (nav, footer, `.frame`, buttons) so it stays self-contained and independently openable. **If you change a token, change it in every page.** That duplication is the deliberate price of having no build step; if the page count grows past three or four, extract a shared stylesheet instead.

Two things a long-form page needs that the card index does not: a scrim behind the fixed nav (`\.nav-bar::before`), because prose scrolls underneath it, and `scroll-margin-top` on sections so anchored links do not land under the bar.

## Design notes

The visual language is deliberately dark-only: `#101010` ground, `#F2F2F2` text, `#3D3D3D` card borders, cards on `linear-gradient(190deg, #252525, #101010)`. Do not add a light theme; the design is committed to one world.

Type is Neue Montreal with a Gloock italic accent, falling back to Helvetica Neue and Georgia Italic where those are not installed.

## Regenerating the share image

`og.png` is produced by a Pillow script using macOS system fonts (`HelveticaNeue.ttc`, index 10 = Medium upright). Regenerate it whenever the name or headline changes, otherwise link previews go stale.

Prose on this site uses no em dashes and no en dashes. Use a colon, a comma, or a full stop, and write year ranges as "2027 to 2028".

Body text must clear 4.5:1 against the background. On this palette `--fg-50` is 4.9:1 and passes; `--fg-30` is 2.5:1 and is for decorative labels only, never for a sentence the reader needs.
