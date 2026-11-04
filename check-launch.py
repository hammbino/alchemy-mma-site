"""Check the live site after the domain switch. Safe to run any time: it only reads.

Run: python3 check-launch.py
     python3 check-launch.py --before   (only the DNS checks that should already pass)

Each line prints OK or FAIL. The script exits with an error if anything failed.
"""
import re
import subprocess
import sys

DOMAIN = "alchemymma.com"
GITHUB_A = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}
GITHUB_AAAA = {"2606:50c0:8000::153", "2606:50c0:8001::153", "2606:50c0:8002::153", "2606:50c0:8003::153"}
EMAIL_MX = {"aspmx.l.google.com.", "alt1.aspmx.l.google.com.", "alt2.aspmx.l.google.com.",
            "alt3.aspmx.l.google.com.", "alt4.aspmx.l.google.com."}
VERIFY_TXT = "google-site-verification=cvxtTP71UfxwO2hpAFM7s_wL-Dats4Py105MAL6Ejyw"

# Our pages, plus the old Gymdesk addresses that people may have saved or found on Google.
PAGES = ["", "classes", "schedule", "coaches", "four7", "coaching", "groups", "pricing", "shop", "about",
         "classes.html", "pricing.html", "sitemap.xml", "robots.txt"]
OLD_ADDRESSES = ["contact", "instructors", "instructors/bio/id/68968", "instructors/bio/id/74699",
                 "page/AboutUs", "page/Future%20Programs", "page/what-we-teach-goes-beyond-the-mats",
                 "signup", "login"]

failures = []


def report(ok, what, detail=""):
    print(("OK   " if ok else "FAIL ") + what + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(what)


def dig(kind, name):
    out = subprocess.run(["dig", "+short", kind, name, "@8.8.8.8"], capture_output=True, text=True).stdout
    return {line.strip() for line in out.splitlines() if line.strip()}


def curl(url, follow=True):
    """Returns (status, final url, body). Stops after 10 redirects, which catches loops."""
    args = ["curl", "-s", "-o", "-", "-w", "\n%{http_code} %{url_effective}", "--max-time", "20"]
    if follow:
        args += ["-L", "--max-redirs", "10"]
    r = subprocess.run(args + [url], capture_output=True, text=True)
    body, _, tail = r.stdout.rpartition("\n")
    code, _, final = tail.partition(" ")
    if r.returncode == 47:
        return "loop", final, body
    if r.returncode == 60:
        return "bad certificate", final, body
    return code, final, body


def check_dns_unchanged():
    mx = {line.split()[-1] for line in dig("MX", DOMAIN)}
    report(mx == EMAIL_MX, "email (MX) records unchanged", f"got {sorted(mx)}")
    report(f'"{VERIFY_TXT}"' in dig("TXT", DOMAIN), "Google verification record still there")


def check_dns_switched():
    report(dig("A", DOMAIN) == GITHUB_A, "alchemymma.com points to GitHub", f"got {sorted(dig('A', DOMAIN))}")
    report(dig("AAAA", DOMAIN) == GITHUB_AAAA, "alchemymma.com IPv6 points to GitHub",
           f"got {sorted(dig('AAAA', DOMAIN))}")
    report(dig("CNAME", "www." + DOMAIN) == {"hammbino.github.io."}, "www points to GitHub",
           f"got {sorted(dig('CNAME', 'www.' + DOMAIN))}")


def check_site():
    for path in PAGES + OLD_ADDRESSES:
        code, final, body = curl(f"https://{DOMAIN}/{path}")
        ours = "four7.html" in body or "This page has moved" in body or path.endswith((".xml", ".txt"))
        report(code == "200" and ours, f"/{path} loads", f"{code} at {final}")
    code, final, body = curl(f"https://{DOMAIN}/")
    report("review-bar" not in body and "data-ask" not in body, "no pink review markers on the home page")
    code, final, _ = curl(f"https://www.{DOMAIN}/")
    report(code == "200" and final.startswith(f"https://{DOMAIN}/"), "www forwards to alchemymma.com",
           f"{code} at {final}")
    code, final, _ = curl(f"http://{DOMAIN}/", follow=True)
    report(final.startswith("https://"), "plain http forwards to https", f"ended at {final}")
    code, _, body = curl(f"https://{DOMAIN}/product/old-gymdesk-link/1", follow=False)
    report(code == "404" and "Page not found" in body, "unknown addresses show our page-not-found page",
           f"{code}")


def check_gymdesk_links():
    """Every Gymdesk link on the site must end on a working Gymdesk page, not loop back to us."""
    links = set()
    for page in ["", "classes", "coaches", "coaching", "four7", "groups", "pricing", "shop", "about",
                 "schedule", "signup", "login"]:
        _, _, body = curl(f"https://{DOMAIN}/{page}", follow=False)
        links |= set(re.findall(r'https://(?:alchemy-mma\.gymdesk\.com|my\.alchemymma\.com)/[^"\'\s<>]*', body))
    report(bool(links), "found Gymdesk links on the site", "none found")
    for url in sorted(links):
        code, final, _ = curl(url)
        lands = final.split("/")[2] if final.count("/") >= 2 else final
        report(code == "200" and lands != DOMAIN, f"Gymdesk link works: {url}", f"{code} at {final}")


if __name__ == "__main__":
    check_dns_unchanged()
    if "--before" not in sys.argv:
        check_dns_switched()
        check_site()
        check_gymdesk_links()
    print()
    print(f"{len(failures)} problem(s)" if failures else "All checks passed.")
    sys.exit(1 if failures else 0)
