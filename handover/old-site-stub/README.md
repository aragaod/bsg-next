# Stub for the old BSG site (bsg.crystallography.org.uk)

For handover step 6, after the committee approves the new site: replace these pages in the old site's repository with the files here.

- `index.html` is a signpost page pointing to https://biostructures.org.uk.
- The other pages redirect straight to their new equivalents and tell search engines where the content has moved (canonical link and an instant redirect):

| Old page | New page |
|---|---|
| `organisation.html` | https://biostructures.org.uk/about/committee/ |
| `archives.html` | https://biostructures.org.uk/meetings/#archive |
| `useful.html` | https://biostructures.org.uk/resources/ |
| `education.html` | https://biostructures.org.uk/training/ |
| `prizes.html` | https://biostructures.org.uk/prizes/ |
| `contact.html` | https://biostructures.org.uk/about/ |

Leave the old programme files (PDF, DOC, RTF) in place so existing links to them keep working; copies are in the new site under `/archive/programmes/`. Delete the backup copies (`*_safe.html`, `*_29mar24.html` and similar).
