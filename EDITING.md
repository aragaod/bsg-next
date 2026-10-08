# Editing the BSG website

The site is edited in the browser with **Pages CMS**. You don't need to know HTML, and you don't need a GitHub account.

**Editor:** <https://app.pagescms.org> · **Website:** <https://biostructures.org.uk> · **This guide, formatted and printable:** <https://biostructures.org.uk/editing/>

---

## For the site administrator: giving someone editing access

1. Sign in at <https://app.pagescms.org> with GitHub and open **aragaod/bsg-next** (branch `main`).
2. In the left sidebar, under **Admin**, choose **Collaborators**.
3. Enter the person's email address and send the invitation.
4. They receive an email titled **Join "aragaod/bsg-next" on Pages CMS** with a link to accept.

To remove access, delete the person from the same Collaborators list.

The Pages CMS GitHub app must stay installed on the `bsg-next` repository (GitHub → Settings → Applications → Pages CMS). If the repository is later transferred to the `bcabsg` organisation, the app needs installing there and collaborators re-inviting.

---

## For editors

### Signing in

1. Open the link in your invitation email, or go to <https://app.pagescms.org>.
2. Choose to sign in with **email** and enter the address the invitation was sent to.
3. You receive a **one-time code** by email. It is valid for 5 minutes. Enter it to sign in.
4. Open **aragaod/bsg-next**.

### What you can edit

| In the sidebar | What it changes on the website |
|---|---|
| **Editor guide (read me)** | This guide. Please read it rather than edit it. |
| **News** | News posts. The newest appears on the home page and in the bar at the top. |
| **Meetings** | Winter Meetings and Spring Meeting sessions, past and future. Setting a **start date** switches on the countdown on the home page; **Deadlines** feed the top bar and the calendar. |
| **Structure of the month** | One entry per month, dated the 1st. Future months stay hidden until their date, so you can prepare them in advance. |
| **Community** | Member spotlights and podcast episodes. |
| **Pages** | The text of About, History, Join, Committee, Community, Chat and Mentoring, and the introductions on Meetings, Training and Resources. |
| **Lists** | The Notice messages in the top bar, events calendar, training courses, committee, prizes and winners, and Resources links. |
| **Media** | Uploaded files. Images are stored in `images`, documents (PDF, Word, PowerPoint) in `archive`; each upload field puts files in the right place automatically. |

### The bar at the top of every page

The dark bar above the menu rotates through short messages. They come from five places, and only the last one is typed in by hand:

| Label in the bar | Where the message comes from | To change it |
|---|---|---|
| **Next meeting** | The soonest upcoming Winter or Spring meeting | Meetings → the meeting → **Start date**, **City** |
| **Deadline** | The next deadline of each upcoming meeting, e.g. "abstracts due 20 November". When it passes, the following deadline replaces it | Meetings → the meeting → **Deadlines** |
| **Structure of the month** | The latest published structure | Structure of the month |
| **News** | The newest news post | News |
| **Notice** | Extra messages typed in by an editor, each shown until its **Show until** date | Lists → Announcements bar |

Messages that depend on the date (a deadline passing, a notice reaching its **Show until** date, a scheduled news post or structure) change at the automatic rebuild each night, just after midnight.

### Making a change

1. Choose a section, then **Add an entry** or **Edit** an existing one.
2. Fill in the form. Each field has a short explanation underneath.
3. Click **Save**.

The website updates about **one to two minutes** after you save. If you don't see the change, reload the page with **Cmd + Shift + R** (Mac) or **Ctrl + Shift + R** (Windows), because browsers keep pages for a few minutes.

Every save is recorded with your name. Mistakes can always be undone, so don't worry about breaking anything; ask the administrator if something looks wrong.

### Common tasks

- **Post news:** News → Add an entry → title, date, a one-sentence summary and the text.
- **Schedule or retire a news post:** a post with a future **Date** stays hidden until that day. Posts stay on the site permanently unless you set **Remove after**, which takes the post down on that date (for short-lived notices such as a deadline reminder).
- **Announce the Winter Meeting date:** Meetings → the meeting → set **Start date** (and **Registration link** when ready). The home page countdown starts straight away, and the meeting appears on the Events page and in subscribers' calendars.
- **Add meeting deadlines:** Meetings → the meeting → **Deadlines** → add one line per deadline, e.g. "Abstracts due" and "Registration closes", each with its date. The next one rotates in the top bar, and every deadline is added to the calendars of people subscribed to the events feed. Don't add a separate Notice for them.
- **Add a meeting programme or poster:** Meetings → the meeting → **Programme** (PDF), **Poster** (image), or **Attachments** for anything else (abstract book, travel info).
- **Attach a PDF to a news post:** News → the post → **Attachments** → link text (e.g. "Poster (PDF)") and upload the file.
- **Point the announcements bar at a PDF:** Lists → Announcements bar → leave **Link** empty and use **Or upload a file**.
- **Add a flyer to an event:** Lists → Events calendar → the event → **Flyer or programme (PDF)**.
- **Database links on the home page images:** Lists → Home page images → **Data**, e.g. `PDB 8QVU · EMD-18657 · SASBDB SASDVA6 · BMRB 34925`; links are added automatically.
- **Add an event from another organisation:** Lists → Events calendar → add an item with a title, organiser, link and dates. Past events disappear by themselves.
- **Schedule a structure of the month:** Structure of the month → Add an entry → date = 1st of the month. Include the PDB IDs; the first one is shown in the 3D viewer.
- **Add a temporary notice to the top bar:** Lists → Announcements bar → add a message with a **Show until** date. Use this for things that are not meeting deadlines, such as a prize call or another organisation's event.
- **Record prize winners:** Lists → Prizes → the prize → Winners → add the year and name.

### Please remember

- **Photos of people only with their permission.** This includes meeting photos and committee portraits.
- **No personal contact details** (phone numbers, home addresses) unless already public and agreed.
- **Credit images**, for example "Image: RCSB PDB, entry 1BMF."
- **Keep it short and plain.** Most visitors read on a phone.
