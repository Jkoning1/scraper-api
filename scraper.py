import requests
from bs4 import BeautifulSoup
import re
import time

def funda_scrape(url):
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "nl-NL,nl;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })

    results = []
    page = 1

    while True:
        print(f"🔎 Scraping pagina {page}...")

        paged_url = f"{url}&page={page}"
        time.sleep(1.4)

        r = session.get(paged_url)
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")

        address_blocks = soup.select("[data-testid='listingDetailsAddress']")
        if not address_blocks:
            print("📭 Geen listings gevonden – stoppen.")
            break

        for ab in address_blocks:
            container = ab.find_parent("div")

            while container and not container.select("ul li span"):
                container = container.find_parent("div")

            if not container:
                continue

            # ADRES
            address_el = ab.select_one(".font-semibold span.truncate")
            address = address_el.get_text(strip=True) if address_el else None

            # LOCATIE
            loc_el = ab.select_one(".text-neutral-80")
            location = loc_el.get_text(strip=True) if loc_el else None

            # PRIJS
            price_el = container.select_one("div.mt-2 .font-semibold .truncate")
            price = price_el.get_text(strip=True) if price_el else None

            # KENMERKEN
            m2 = None
            bedrooms = None
            energy = None
            
            m2_candidates = []

            for s in container.select("ul li span"):
                t = s.get_text(strip=True)

                # ALLE M² WAARDEN VERZAMELEN
                if "m²" in t:
                    nums = re.findall(r"\d+", t.replace(".", ""))
                    if nums:
                        value = int(nums[0])
                        # Nieuwbouw perceel -> skip extreem grote waarden
                        if value > 300:   # perceelwaarde
                            continue
                        if value >= 20:   # geen rare 1 m²
                            m2_candidates.append(value)

                # ENERGIELABEL
                elif len(t) == 1 and t.isalpha():
                    energy = t

                # SLAAPKAMERS (digits)
                elif t.isdigit():
                    bedrooms = int(t)

            # KLEINSTE M² = woonoppervlakte
            if m2_candidates:
                m2 = min(m2_candidates)

            results.append({
                "address": address,
                "location": location,
                "price": price,
                "m2": m2,
                "bedrooms": bedrooms,
                "energy_label": energy,
            })

        page += 1

    return results

# --- VOORBEELD ---
if __name__ == "__main__":
    url = "https://www.funda.nl/zoeken/koop?custom_area=yqiZ%257Df_%257CHoXrDvn%2540pa%2540zRqHci%2540s%255D"
    data = funda_scrape(url)

    for d in data:
        print(d)
