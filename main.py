import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINE_STORE_BIRTH_DATE = 1920
TEMPLATE_NAME = "template.html"
RESULT_FILE_NAME = "index.html"
EXCEL_FILE_NAME = "wine3.xlsx"

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template(TEMPLATE_NAME)

wine_store_age = datetime.datetime.today().year - WINE_STORE_BIRTH_DATE
excel_wine_data = pandas.read_excel(EXCEL_FILE_NAME)
wine_items = excel_wine_data.to_dict(orient='record')

grouped_wine_items = defaultdict(list)
for item in wine_items:
    grouped_wine_items[item['Категория']].append(item)

rendered_page = template.render(
    wine_items=grouped_wine_items,
    wine_store_age=wine_store_age
)

with open(RESULT_FILE_NAME, 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
