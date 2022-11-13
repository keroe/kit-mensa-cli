from .kit_mensa import *

def main():
    URL = (
        "https://www.mensaplan.de/karlsruhe/mensa-am-adenauerring/index.html"
    )
    mensa_webpage_html = get_mensa_webpage_as_html(URL)
    mensa_menu_dict = filter_menus_from_webpage(mensa_webpage_html)
    weekday_idx = get_weekday_as_index()
    mensa_table = get_menu_for_today(mensa_menu_dict, weekday_idx)
    print(mensa_table)


if __name__ == "__main__":
    main()
