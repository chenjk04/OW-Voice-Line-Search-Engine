# Overwatch Wiki contributors. (n.d.). Fandom.
# https://overwatch.fandom.com/wiki/Overwatch_Wiki

# table class = "listtable"
# tr -> td[-2] is text, td[-1] -> audio source (possibly DNE)

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
import json

ID_COUNTER = 0

HERO_LIST = [
    "Ana",
    "Anran",
    "Ashe",
    "Baptiste",
    "Bastion",
    "Brigitte",
    "Cassidy",
    "D.Va",
    "Domina",
    "Doomfist",
    "Echo",
    "Emre",
    "Freja",
    "Genji",
    "Hanzo",
    "Hazard",
    "Illari",
    "Jetpack Cat",
    "Junker Queen",
    "Junkrat",
    "Juno",
    "Kiriko",
    "Lifeweaver",
    "Lúcio",
    "Mauga",
    "Mei",
    "Mercy",
    "Mizuki",
    "Moira",
    "Orisa",
    "Pharah",
    "Ramattra",
    "Reaper",
    "Reinhardt",
    "Roadhog",
    "Sierra",
    "Sigma",
    "Sojourn",
    "Soldier: 76",
    "Sombra",
    "Symmetra",
    "Torbjörn",
    "Tracer",
    "Venture",
    "Vendetta",
    "Widowmaker",
    "Winston",
    "Wrecking Ball",
    "Wuyang",
    "Zarya",
    "Zenyatta"
]


def load_html(hero_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://overwatch.fandom.com/wiki/{hero_name}/Quotes")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()
    return soup


def locate_rows(hero_name, soup):
    header = soup.find("span", id="Voice_Lines")
    if header is None:
        print(f"{hero_name}: Voice_Lines section not found")
        return
    h2 = header.find_parent("h2")
    table = h2.find_next("table", class_="listtable")
    if table is None:
        print(f"{hero_name}: table not found")
        return
    rows = table.find_all("tr")
    return rows


def parse_table(hero_name, rows):
    output = []
    id_counter = 0;
    for row in rows:
        tds = row.find_all("td")

        if len(tds) < 2:
            continue

        line_text = tds[-2].get_text(" ", strip=True)
        source_tag = tds[-1].find("source")
        if source_tag and source_tag.has_attr("src"):
            audio_url = source_tag["src"]
        else:
            audio_url = None

        if line_text:
            output.append({
                "hero":hero_name,
                "ID":make_id(hero_name, id_counter),
                "line":line_text,
                "audio_url":audio_url
            })
        
        id_counter+=1
    
    return output


def output_json(hero_name, output):
    output_file = f"backend/data/voicelines_json/{hero_name}_quotes.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return


def make_id(hero, line):
    str = f"{hero}_{line}"
    return hashlib.md5(str.encode()).hexdigest()


def scrape(hero_name):
    soup = load_html(hero_name)
    rows = locate_rows(hero_name, soup)
    output = parse_table(hero_name, rows)
    output_json(hero_name, output)


def main():
    for hero in HERO_LIST:
        scrape(hero)


if (__name__ == "__main__"):
    main()





