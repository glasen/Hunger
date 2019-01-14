#!/usr/bin/env python3
def main():
    parser = argparse.ArgumentParser(description="Wir haben Hunger, Hunger, Hunger ...")
    parser.add_argument("--mensa", "-m", help="Welche Mensa?", default="THM",
                        choices=["THM", "MILF", "Campustor", "IFZ", "CaRe", "OBS"], nargs="*")

    parser.add_argument("--woche", "-w", help="Bunte Wochenübersicht ...", action='store_true', required=False)

    mensen = {"THM": "giessen_thm", "Campustor": "giessen_campustor", "MILF": "giessen_mfhf", "IFZ": "giessen_cafeifz",
              "CaRe": "giessen_cafecare", "OBS": "giessen_obs_tage"}

    args = parser.parse_args()
    mensa_list = args.mensa
    week_set = args.woche

    home = str(Path.home())

    if os.path.isfile(home + "/.hunger"):
        parsed_list = _parse_hunger_config_file(home + "/.hunger", mensen)
        if len(parsed_list) != 0:
            mensa_list = parsed_list
        else:
            print("Fehler in der Konfigurationsdatei. Keine gültigen Einträge gefunden!")
            exit(1)

    for mensa in mensa_list:
        mensa_id = mensen[mensa]
        html_string = download_food_menu(mensa_id)
        food_dict = get_food_menu(html_string)

        if week_set:
            for dates, menus in food_dict.items():
                year, year_day = dates
                _get_menus(mensa, menus, year, year_day)
                print()
        else:
            year = datetime.today().timetuple().tm_year
            year_day = datetime.today().timetuple().tm_yday

            menus = food_dict[(year, year_day)]

            if len(menus) == 0:
                print("Heute kein Essen!")
            else:
                _get_menus(mensa, menus, year, year_day)

        print()


def download_food_menu(mensa_id):
    url = "https://giessen.my-mensa.de/essen.php?&lang=de&mensa=" + mensa_id + "#" + mensa_id

    http = urllib3.PoolManager()
    urllib3.disable_warnings()

    r = http.request("GET", url)

    return r.data.decode()


def get_food_menu(html_string):
    day_numbers = _get_days_from_week_number()

    parser = etree.HTMLParser()
    root = etree.parse(StringIO(html_string), parser)

    day_pattern = re.compile(r"_(\d*)_")

    food_dict = defaultdict(list)

    for child in root.findall(".//body//div[@data-role='content']//a"):

        prefixes = list()
        suffixes = list()

        food_link = child.attrib.get("href")

        if food_link is not None and food_link.startswith("detail"):

            year_day = day_pattern.findall(food_link)[0]

            year = int(year_day[:4])
            day = int(year_day[4:]) + 1

            for h in child.findall(".//h3[@class='ct ui-li-heading']"):
                prefix = h.text.replace("\xad", "").strip()
                prefixes.append(prefix)

            for p in child.findall(".//p[@class='ct']"):
                suffix = p.text
                if suffix is not None:
                    suffix = suffix.replace("\xad", "").strip()
                else:
                    suffix = ""

                suffixes.append(suffix)

            merged = _merge_lists(prefixes, suffixes)
            if not merged.startswith("Beilagenauswahl") and day in day_numbers:
                food_dict[(year, day)].append(merged)

    return food_dict


def _parse_hunger_config_file(filename, mensen):
    file = open(filename, "r")
    lines = file.read()
    config_list = lines.strip().split("\n")

    return list(set(config_list) & set(mensen.keys()))


def _get_menus(mensa, menus, year, year_day):
    print(mensa, "-", _get_date(year, year_day) + " :")
    for index, menu in enumerate(menus):
        print("\t", index + 1, menu)


def _get_date(year, year_day):
    t = datetime.strptime(str(year) + " " + str(year_day), '%Y %j')
    return t.strftime('%a %d.%m.%Y')


def _get_days_from_week_number():
    weekday = datetime.today().weekday()
    day_of_year = datetime.now().timetuple().tm_yday
    start = day_of_year - weekday
    end = start + 6

    return [i for i in range(start, end)]


def _merge_lists(prefixes, suffixes):
    suffix = ""
    prefix = ""
    for i in range(len(prefixes)):
        prefix = prefixes[i]
        suffix = suffixes[i]

    return " ".join([prefix, suffix])


if __name__ == "__main__":
    import argparse
    import urllib3
    import re
    import locale
    import os.path
    from pathlib import Path

    from lxml import etree
    from io import StringIO
    from collections import defaultdict
    from datetime import datetime

    locale.setlocale(locale.LC_ALL, '')

    main()
