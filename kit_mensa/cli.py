import kit_mensa

if __name__ == "__main__":
    KIT_MENSA_URL = (
        "https://www.mensaplan.de/karlsruhe/mensa-am-adenauerring/index.html"
    )
    mensa_webpage_html = kit_mensa.get_mensa_webpage_as_html(KIT_MENSA_URL)
    mensa_menu_dict = kit_mensa.filter_menus_from_webpage(mensa_webpage_html)
    weekday_idx = kit_mensa.get_weekday_as_index()
    mensa_table = kit_mensa.get_menu_for_today(mensa_menu_dict, weekday_idx)
    print(mensa_table)
