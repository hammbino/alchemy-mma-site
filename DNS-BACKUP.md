# alchemymma.com DNS before the switch

Copied from Squarespace (Domains > alchemymma.com > DNS) on 2026-11-03, before any change.
To undo the switch, put the two custom records back exactly as below.

## Custom records (the only ones we change)
| Type | Name | TTL | Data |
|---|---|---|---|
| A | @ | 4 hrs | 45.79.19.164 |
| CNAME | www | 4 hrs | alchemymma.com |

## Leave these alone
| Group | Type | Name | Priority | TTL | Data |
|---|---|---|---|---|---|
| Squarespace Domain Connect | CNAME | _domainconnect | | 1 hr | _domainconnect.domains.squarespace.com |
| Domain Connect to Google | TXT | @ | | 1 hr | google-site-verification=cvxtTP71UfxwO2hpAFM7s_wL-Dats4Py105MAL6Ejyw |
| Google Workspace (email) | MX | @ | 1 | 4 hrs | aspmx.l.google.com |
| Google Workspace (email) | MX | @ | 5 | 4 hrs | alt1.aspmx.l.google.com |
| Google Workspace (email) | MX | @ | 5 | 4 hrs | alt2.aspmx.l.google.com |
| Google Workspace (email) | MX | @ | 10 | 4 hrs | alt3.aspmx.l.google.com |
| Google Workspace (email) | MX | @ | 10 | 4 hrs | alt4.aspmx.l.google.com |
