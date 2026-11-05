# Gymdesk site backup

Saved 2026-11-03, right after the switch, before any change to the Gymdesk homepage.
Each file is the page as visitors saw it at my.alchemymma.com (formerly alchemymma.com).

To restore the old Gymdesk homepage: Gymdesk > Website > Homepage > "Current Revision" menu >
pick Revision 40 (07/01/2026 2:27pm) > Publish. These files are the fallback if that history is gone.

To restore the old menu: Website > Settings > Website Navigation, turn About, Schedule,
Instructors, Contact, and Pricing back on, then Save Settings.

## Website Settings before the 2026-11-03 cleanup
| Field | Old value |
|---|---|
| Logo link | (empty) |
| Font | Helvetica |
| Background / text / link / button colors | #000000 / #c9a24a / #c9a24a / #c9a24a (secondary text #4a4340) |
| Instagram | alchemy.mma |
| Facebook | (empty) |
| Head scripts / Body scripts | (empty) |
| Website title | Alchemy MMA \| Jiu-Jitsu, Striking & MMA in American Fork, Utah (shown with repeated &amp;amp;) |

Pages "Upcoming Programs", "WHAT WE TEACH GOES BEYOND THE MATS", and "About Alchemy" had
"Show in website menu" on. To restore: Website > Pages > Edit > Page Settings > turn it on > Publish.

Body scripts added 2026-11-03: a short script that points the header logo and name at https://alchemymma.com/. Head scripts: Google Fonts (Marcellus, Archivo) and a style block. Clear both boxes to undo.

Head scripts also set the tab and home-screen icons to the alchemymma.com emblem (favicon.ico, img/icon-192.png, apple-touch-icon.png), overriding Gymdesk's default icon.

Head scripts, added 2026-11-04: a first line that forwards the my.alchemymma.com homepage ("/") to https://alchemymma.com/.
Why: Gymdesk ignores the Logo link setting and our scripts on the login, signup, and shop pages, so their logo always links to "/".
Forwarding "/" makes that logo land on the main site. To undo, delete the first `<script>` line in Head scripts and Save Settings.
