# Alchemy MMA website: project handoff

Read this first in every session. It holds the context, the current state, and what's next,
so Jeffrey doesn't have to re-explain. Update the **Current status** and **Open items** sections
whenever something changes, and commit the update.

Last updated: 2026-11-03.

## The short version

- The new site is **live at https://alchemymma.com** (switched 2026-11-03, about 9:20pm MST).
- Gymdesk (signup, login, shop, program forms, schedule) runs at **https://my.alchemymma.com**.
- What's left is content from Brian (see **Open items**), plus a few optional improvements.

## People

- **Brian and Maryann Thomas** own Alchemy MMA in American Fork, Utah. Brian is the head coach.
  Brian gets short text messages. He doesn't follow technical terms, so give him plain, click-by-click steps.
- **Jeffrey** (the user) builds and runs the site. He trained with Brian in the early Lehi gym with his son.
- **Rad** and **Micah** are coaches. **Jason Mertlich** created the Four7 System.
- Gym: 329 S 860 E Suite 1, American Fork, UT 84003. Phone (385) 202-6561. Brian@alchemymma.com.
  Facebook: https://www.facebook.com/profile.php?id=61595633090501. Instagram: https://www.instagram.com/alchemy.mma/

## How Jeffrey wants to work

- Plain English. Short sentences. Lead with the answer. **No em dashes.** No emojis in anything people will read.
- Texts to Brian are short. Anything Brian has to do comes as simple numbered steps.
- Posts and reviews must sound like a person wrote them. Don't invent facts.
- **Site facts come only from Brian, the old site** (saved in `gymdesk-backup/`)**, or the gym's own Instagram** (saved in `photos/instagram/posts.json`). Anything found elsewhere, like outside research, goes to Brian as a question (`data-ask`). Don't publish it until he confirms.
- "Start your free week" button (2026-11-04): it's in the header on every page, and a sticky bottom bar on phones. Claude added both in the first build without being asked. Jeffrey decided to keep both unless Brian says otherwise.
- Tagline (Jeffrey's call, 2026-11-03): "Martial arts is the vehicle. Personal growth is the destination."
- Check before claiming something works. Show the result and let Jeffrey decide when it's done.
- The usual workflow is to commit and push to `main`. Pushing publishes the live site.
- Ask before changing anything outside the repo (DNS, Gymdesk, GitHub settings) unless Jeffrey said to do it.

## Accounts and access

- **GitHub:** repo `hammbino/alchemy-mma-site`. The `gh` CLI is logged in. Pushing to `main` runs `.github/workflows/`, which builds and deploys to GitHub Pages.
- **Squarespace** (DNS for alchemymma.com) and **Gymdesk** (app.gymdesk.com, the Brian@alchemymma.com account) are both open in Jeffrey's Chrome.
  Claude can drive them with the Chrome tools, but can't type passwords or sign in.
  Squarespace asks Jeffrey to "Verify with Google" before most DNS edits. Jeffrey clicks Continue, then Claude edits.
- Claude Code's safety check sometimes blocks DNS or GitHub Pages domain changes. When that happens, give Jeffrey exact click steps instead.

## How the site works

- Page content: `src/pages/*.html`. Each page starts with front matter: `title`, `seo_title`, `nav`, `description`.
- Shared header and footer: `src/layout.html`. Styles: `site/styles.css`. Script: `site/main.js`. Images: `site/img/` (edited directly, not generated).
- `python3 build.py` builds everything into `site/`:
  - SEO tags, business details for Google (home page only), `sitemap.xml`, `robots.txt`
  - redirect pages for old Gymdesk addresses (`REDIRECTS`)
  - `404.html`
  - `FOR-BRIAN.md`
- **Questions for Brian:** put `data-ask="question"` on the element in `src/pages/`. `build.py` collects these into `FOR-BRIAN.md`.
  `LAUNCHED = True` hides the pink markers on the live site. When Brian answers, update the content and remove the `data-ask`.
  Other things we're waiting on go in `FOLLOW_UPS` in `build.py`.
- All Gymdesk links use `https://my.alchemymma.com/...` (the `GYMDESK` constant in `build.py` and in the page files).
- `python3 check-launch.py` checks DNS, email records, every page, old addresses, the 404 page, and every Gymdesk link. It's safe to run anytime and should print "All checks passed."

## Current status (2026-11-03)

**Live and verified:**
- **DNS (Squarespace):**
  - `@` has GitHub's 4 A records (185.199.108-111.153) and 4 AAAA records.
  - `www` CNAME points to `hammbino.github.io`.
  - `my` A record points to 45.79.19.164 (Gymdesk).
  - Google Workspace email (MX) and the google-site-verification TXT are untouched.
- **GitHub Pages:** custom domain alchemymma.com. The certificate covers alchemymma.com and www. HTTPS is enforced.
- **Gymdesk:** custom domain my.alchemymma.com, SSL active.
  - Menu: Shop, Login, Signup.
  - The 3 custom pages (Upcoming Programs, What We Teach, About Alchemy) are hidden from the menu but still published.
  - Homepage: logo, "Alchemy MMA has a new website", and a button to alchemymma.com.
    Since 2026-11-04 a head script forwards that homepage straight to alchemymma.com, so visitors never see it.
  - Head scripts load the site's fonts (Marcellus, Archivo) and the tab icons. A body script points the header name at alchemymma.com.
  - Gold #D9A73C. Instagram and Facebook links fixed.
- **Tab icons:** square emblem `favicon.ico`, `img/icon-192.png`, `apple-touch-icon.png`.

**Sent to Brian (2026-11-03):** a text saying the switch is done, the 6 open items below, and steps to submit the sitemap in Google Search Console.

## Open items

**Waiting on Brian** (the full list is in `FOR-BRIAN.md`):
1. Micah's photo and full bio (coaches page)
2. Jason's feedback on the Four7 page. Also ask whether to add the outside-research claims that were pulled 2026-11-03: developed in Utah, no-gi combat Jujitsu built for fights with strikes, control and finishing rather than points.
3. Family discount percentages (pricing page)
4. Google review link, plus reviews to feature. Then build a reviews section on the home page from hand-picked reviews, not a paid widget.
5. A check of the Precision Nutrition description (coaches and 1-on-1 pages)
6. Whether the 10% military/first responder discount is memberships only
6a. Rad's bio: we found Clarion University, three-time NCAA qualifier, and Bellator in outside research. They're not on the site. Ask Brian if they're right and should be added. Not sent to Brian yet.
7. Google Search Console: Brian submits `sitemap.xml`. If he gets a verification code instead, Claude adds the TXT record in Squarespace.
8. From 2026-10-30: Google Business Profile hours and photos, Apple Maps and Yelp listings (turn on Yelp's military discount filter), and point the Instagram and Facebook bios to alchemymma.com.

**Waiting on Jeffrey's decision:**
- `SITE-COMPARISON.md`: all done (fixes 1 to 3 made, Rad and tagline questions added for Brian).
- Whether to fully unpublish the 3 hidden Gymdesk pages (they're still reachable by direct link and Google).

## Backups and undo

- `DNS-BACKUP.md`: the DNS records before the switch.
- `gymdesk-backup/`: every Gymdesk page as it was, plus `README.md` with the old values of every Gymdesk setting and restore steps.
  The old Gymdesk homepage is Revision 40 in Gymdesk's revision history.
- Git history has every site change.

## Gotchas

- Gymdesk's login, signup, and shop pages skip our head and body scripts and the Logo link setting. Their logo always links to "/". That's why "/" forwards to alchemymma.com.
- Gymdesk turns "&" into "&amp;" every time Website Settings is saved. Keep "&" out of the Gymdesk website title.
- Gymdesk's Unpublish/Delete links may open a browser confirm dialog, which freezes the Chrome tools. Use page settings toggles instead, or warn Jeffrey first.
- A stale DNS cache on Jeffrey's Mac or router can show Gymdesk's "Did you find a broken link?" page at alchemymma.com. That's cache, not the site. `check-launch.py` resolves through Google DNS to avoid it.
- Safari caches tab icons for a long time.
- zsh doesn't split variables into words. Use arrays for curl options (for example `R=(--resolve ...)`).
