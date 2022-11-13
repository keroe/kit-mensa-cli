#!/usr/bin/python
import requests
import bs4
import datetime

class MensaLine():
    def __init__(self, name):
        self.name =name
        self.meals = []

    def add_meal(self, meal):
        self.meals.append(meal)

    def get_string_list(self):
        # construct header for line name
        return_string_list = [f"{40*'-'}", f"{self.name}", f"{40*'-'}"]
        # add each in meal with an appending dash
        for meal in self.meals:
            return_string_list.append(f"- {meal}")
        return return_string_list

class MensaTable():
    def __init__(self):
        self.lines = []
    def add_line(self, line):
        self.lines.append(line)

    def __str__(self):
        return_string = ""
        # use an interator here to iterate over two items at the same time. Useful for the 2 column print in the terminal
        it = iter(self.lines)
        for x in it:
            left_rows = x.get_string_list()
            right_rows = next(it).get_string_list()
            for lines_on_left_row, lines_on_right_row in zip(left_rows, right_rows):
                # construct string with content in the left column and the right column with padding in between
                return_string += f"{lines_on_left_row:<100}{lines_on_right_row}\n"
        return return_string

def get_mensa_webpage_as_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text,"html.parser")

def filter_menus_from_webpage(webpage_html):
    # use html class name with a browser analyzing tool to get all columns with meals
    table_columns = webpage_html.find_all("tr", {"class": "today"})
    mensa_menu_dict =  dict()
    for i, column in enumerate(table_columns[1:]):
        meals_per_day_for_line = column.find_all("td")
        # if there are no "td" elements in that column it is a mensa line header
        if not meals_per_day_for_line:
            line_name = column.text
            # construct per line list with one element per weekday
            mensa_menu_dict[line_name] = [[], [], [], [], []]
        for day_idx, meals in enumerate(meals_per_day_for_line):
            for meal in meals:
                meal_text = meal.select_one(".description").text
                # if the meal name is to long, split it after 50 characters for better printing
                if len(meal_text) > 100:
                    meal_text_1 = meal_text[:50]
                    meal_text_2 = meal_text[51:]
                    mensa_menu_dict[line_name][day_idx].append(meal_text_1)
                    mensa_menu_dict[line_name][day_idx].append(meal_text_2)
                else:
                    mensa_menu_dict[line_name][day_idx].append(meal_text)
    return mensa_menu_dict

def get_weekday_as_index():
    # returns weekday as int between 0-6
    return datetime.date.today().weekday()

def get_menu_for_today(mensa_menu_dict, weekday_idx):
    mensa_table = MensaTable()
    for line_name, meals_per_day in mensa_menu_dict.items():
        line_per_day = MensaLine(line_name)
        # for some lines there is only one entry per week -> the meal is the same for every day
        if meals_per_day.count([]) == 4:
            for meal in meals_per_day[0]:
                line_per_day.add_meal(meal)
        # normal lines have an entry for each day
        else:
            for meal in meals_per_day[weekday_idx]:
                line_per_day.add_meal(meal)
        mensa_table.add_line(line_per_day)
    return mensa_table