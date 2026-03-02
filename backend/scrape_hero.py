# Overwatch Wiki contributors. (n.d.). Fandom.
# https://overwatch.fandom.com/wiki/Overwatch_Wiki

# table class = "listtable"
# tr -> td[-2] is text, td[-1] -> audio source (possibly DNE)

from bs4 import BeautifulSoup
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

def scrape(hero_name):
    global ID_COUNTER
    input_file =  f"backend/data/wiki_html/{hero_name}_quotes_wiki.html"
    output_file = f"backend/data/voicelines_json/{hero_name}_quotes.json"
    output = []
    with open(input_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

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
                "ID":ID_COUNTER,
                "line":line_text,
                "audio_url":audio_url
            })
        
        ID_COUNTER+=1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    return

def main():
    # for hero in HERO_LIST:
    #     scrape(hero)
    scrape("D.Va")

if (__name__ == "__main__"):
    main()





