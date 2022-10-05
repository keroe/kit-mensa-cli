#!/usr/bin/python
import requests
import bs4
import re
import copy
import sys
import datetime
import operator
from colored import fg, bg, attr
color_blue = fg('blue')
color_white = attr(0)
url = 'https://www.mensaplan.de/karlsruhe/mensa-am-adenauerring/index.html'
res = requests.get(url)
res.raise_for_status()
mensa_html = bs4.BeautifulSoup(res.text,"html.parser")

table_food = mensa_html.find_all("table",  {"class":"aw-weekly-menu"})
table_columns = mensa_html.find_all("tr", {"class": "today"})
table_dict = {}
lines_to_keep = []

class MensaLine():
    def __init__(self, name):
        self.name =name
        self.meals = []

    def add_meal(self, meal):
        self.meals.append(meal)

    def get_string_list(self):
        return_string_list = [f"{40*'-'}", f"{self.name}", f"{40*'-'}"]
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
        it = iter(self.lines)
        for x in it:
            left_row = x.get_string_list()
            right_row = next(it).get_string_list()
            for l, r in zip(left_row, right_row):
                return_string += f"{l:<100}{r}\n"
        return return_string


for i,column in enumerate(table_columns[1:]):
    meals_per_day_for_line = column.find_all("td")
    if not meals_per_day_for_line:
        line_name = copy.copy(column.text)
        table_dict[line_name] = [[], [], [], [], []]
    for l, meals in enumerate(meals_per_day_for_line):
        for meal in meals:
            meal_text = meal.select_one(".description").text
            if len(meal_text) > 100:
                meal_text_1 = meal_text[:50]
                meal_text_2 = meal_text[51:]
                table_dict[line_name][l].append(meal_text_1)
                table_dict[line_name][l].append(meal_text_2)
            else:
                table_dict[line_name][l].append(meal_text)

day_idx = datetime.date.today().weekday()
mensa_table = MensaTable()
for line_name, meals_per_day in table_dict.items():
    line_per_day = MensaLine(line_name)
    if meals_per_day.count([]) == 4:
        for meal in meals_per_day[0]:
            line_per_day.add_meal(meal)
    else:
        for meal in meals_per_day[day_idx]:
            line_per_day.add_meal(meal)
    mensa_table.add_line(line_per_day)

print(mensa_table)