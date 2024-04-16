#!/usr/bin/python
import requests
import bs4

from rich.panel import Panel
from rich.table import Table


def get_emoji_based_on_icon(icon):
    icon_to_emoji_dict = {
        "enthält regionales Rindfleisch aus artgerechter Tierhaltung": ":cow_face:",
        "enthält Schweinefleisch": ":pig_face:",
        "MSC aus zertifizierter Fischerei": ":fish:",
        "vegetarisches Gericht": "🥚 :seedling:",
        "veganes Gericht": ":seedling:",
    }
    try:
        return_value = icon_to_emoji_dict[icon]
    except KeyError:
        return_value = ""
    return return_value


def get_menu_renderable(mensa_menu_dict):
    renderables = []
    for line, meals in mensa_menu_dict.items():
        table = Table(box=None)
        for meal in meals:
            emoji = get_emoji_based_on_icon(meal["icon"])
            table.add_row(
                f"{emoji}",
                f"{meal['meal']}",
                f"{meal['price']} €" if meal.get("price") else "",
                f"{meal['extras'] if meal.get('extras') else ''}",
            )
        renderables.append(Panel(table, title=f"[b]{line}", height=len(table.rows)+3))
    return renderables


def get_mensa_webpage_as_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, "html.parser")


def filter_menus_from_webpage(webpage_html):
    import re

    # use html class name with a browser analyzing tool to get the current day menu table
    current_day_html = webpage_html.find("div", {"id": "canteen_day_1"})
    # filter by mensa line rows
    table_rows = current_day_html.find_all("tr", {"class": "mensatype_rows"})
    mensa_menu_dict = dict()
    for row in table_rows[:5]:
        # get the line name and convert <br> to " "
        line_name = row.find("td", {"class": "mensatype"}).get_text(" ")
        mensa_menu_dict[line_name] = []
        # all meal table row elements start with mt-
        meals_html = row.find_all("tr", {"class": lambda L: L and L.startswith("mt-")})
        for meal_html in meals_html:
            meal_icon_html = meal_html.find("td", {"class": "mtd-icon"})
            meal_icon = meal_icon_html.find("img")
            meal_title_raw = meal_html.find("td", {"class": "menu-title"})
            meal_price_raw = meal_html.find("span", {"class": "bgp price_1"})
            # meal_title_raw can look like this:
            # "Spaghett [1,3,Ge,ML,Se,We]" where the numbers and chars in the brackets indicate extras
            # use regex to filter actual dish and extras
            meal_title = re.search("^[^\[]+", meal_title_raw.text)
            meal_extras = re.search("\[(.*?)\]", meal_title_raw.text)
            meal_price = re.search("[\d,]+", meal_price_raw.text)
            mensa_menu_dict[line_name].append(
                {
                    "meal": meal_title.group(0) if meal_title else "",
                    "extras": meal_extras.group(0) if meal_extras else "",
                    "icon": meal_icon.get("title") if meal_icon else "",
                    "price": meal_price.group(0) if meal_price else "",
                }
            )
    return mensa_menu_dict
