# Biological Structures Group website

Website of the Biological Structures Group (BSG) of the British Crystallographic Association, at https://biostructures.org.uk. Approved by the BSG committee in October 2026 as the group's main site, replacing bsg.crystallography.org.uk.

Built with [Hugo](https://gohugo.io/) and [Tailwind CSS](https://tailwindcss.com/), deployed to GitHub Pages by GitHub Actions.

## Local preview

Needs Hugo extended (0.166 or later) and Node.js.

```sh
npm ci
hugo server
```

Then open http://localhost:1313/.

## Layout

- `content/` — pages, in Markdown
- `data/` — structured data files (see below)
- `static/archive/` — programmes of past meetings and other historical documents
- `layouts/` — Hugo templates
- `assets/css/main.css` — Tailwind entry point and BSG colour palette
- `.github/workflows/deploy.yml` — build and deploy to GitHub Pages

While `params.noindex` is `true` in `hugo.yaml`, the site asks search engines not to index it.

## Content model

Items that need their own page are Markdown files; simple lists are YAML data files.

| What | Where | Notes |
|---|---|---|
| Meetings (BSG Winter Meeting, BSG sessions at the BCA Spring Meeting) | `content/meetings/YYYY-winter.md`, `YYYY-spring.md` | Leave `start` empty until the date is confirmed: the site shows "date to be confirmed". Meetings move from Upcoming to the Archive automatically. |
| News | `content/news/YYYY-MM-DD-slug.md` | |
| Structure of the month | `content/structures/YYYY-MM-slug.md` | Date it the 1st of its month. Future entries stay hidden until their date; a daily scheduled build publishes them, so a year can be queued in advance. Images from RCSB PDB are CC0 (credit the entry). |
| Podcast episodes | `content/community/podcast/slug.md` | `audio` (MP3 URL) plays in a plain audio player: no third-party embeds. |
| Community pages (chat, mentoring) | `content/community/*.md` | Optional `status` (e.g. "Proposal") shows a badge next to the title. |
| Member spotlights | `content/community/spotlights/slug.md` | Role, institution, techniques, optional photo (only with permission), and a list of questions and answers. |
| Announcements bar | `data/announcements.yaml` | Extra messages with an optional `until` date; the next meeting, structure of the month and latest news are added automatically. |
| Events calendar (other organisations) | `data/events.yaml` | Past events are hidden automatically. |
| Training courses | `data/training.yaml` | |
| Committee | `data/committee.yaml` | Set `confirmed: true` once checked with the Secretary. Photos only with permission. |
| Prizes and winners | `data/prizes.yaml` | |
| Technique tags | `data/techniques.yaml` | Shared list used by events, training and structures. |
| New UK structures feed | `data/uk_structures.json` | **Automatic, don't edit.** Updated every Monday by `.github/workflows/uk-structures.yml` running `scripts/uk_structures.py`: PDB entries funded by UK organisations or with data collected at Diamond (with EMDB IDs for cryo-EM), and SASBDB entries measured at UK facilities. Images are downloaded at build time, not stored in the repo. |

Each data file has a comment block at the top describing its fields. `hugo new meetings/2027-winter.md` (or `news/…`, `structures/…`) creates a file with all fields filled in.

Links inside Markdown can be written as site paths, e.g. `[Meetings](/meetings/)`; they are resolved to work wherever the site is hosted.

## Editing with Pages CMS

Committee members edit the site in the browser at [app.pagescms.org](https://app.pagescms.org); no HTML or Markdown knowledge is needed. The forms are defined in `.pages.yml`.

- **Editors** are invited from Pages CMS (repository settings → collaborators) by email and sign in with a link sent to that address; a GitHub account is optional. Repository collaborators on GitHub can also sign in with GitHub.
- **Saving** commits the change to the `main` branch; the site rebuilds and is live in about a minute.
- **Uploads**: images go to `static/images/`, documents (programmes, PDFs) to `static/archive/`. Only upload photos of people with their permission.
- Saving a YAML list in the editor rewrites the file, so comments at the top of files in `data/` may be removed; field descriptions live in `.pages.yml` and in the table above.

## Search engines and sharing

Built in: a title and description on every page (from the `description` or `summary` fields, or generated for meetings), link previews for social media and email (`static/images/social-card.png`, or a page's own image), structured data (organisation on the home page, events for dated meetings, articles for news and structures), an automatic sitemap with last-updated dates, and redirects from the old site's page names (`/organisation.html` and so on). `handover/old-site-stub/` holds the pages to put on the old site at launch.

## Going live (approved October 2026)

1. In `hugo.yaml`, set `params.noindex: false`. This lets search engines in, adds the sitemap to `robots.txt`, and removes the "draft mockup" footer notice.
2. Add the site to [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters), verified by a DNS TXT record, and submit `https://biostructures.org.uk/sitemap.xml`.
3. Replace the old site's pages with `handover/old-site-stub/`.
4. Ask the BCA and partner sites to link to the new address (see the link-sharing plan in the project brief).
