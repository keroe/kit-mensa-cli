from rich.console import Console
from rich.columns import Columns
from kit_mensa.kit_mensa import get_mensa_webpage_as_html, filter_menus_from_webpage, get_menu_renderable


def main():
    URL = "https://www.sw-ka.de/de/hochschulgastronomie/speiseplan/mensa_adenauerring/"
    mensa_webpage_html = get_mensa_webpage_as_html(URL)
    mensa_menu_dict = filter_menus_from_webpage(mensa_webpage_html)
    mensa_table_renderables = get_menu_renderable(mensa_menu_dict)
    console = Console()
    console.print(Columns(mensa_table_renderables, equal=True))


if __name__ == "__main__":
    main()
