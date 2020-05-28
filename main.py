import argparse
import datetime
import math
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINE_STORE_BIRTH_YEAR = 1920
TEMPLATE_NAME = "template.html"
RESULT_FILE_NAME = "index.html"


def get_jinja_template(file_name):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(file_name)


def get_wines(data_file_name):
    excel_wine_data = pandas.read_excel(data_file_name)
    wines = excel_wine_data.to_dict(orient='record')
    filtered_wines = []
    for wine in wines:
        filtered_wines.append({key: value for key, value in wine.items()
                             if not isinstance(value, float) or not math.isnan(value)})
    wines_by_category = defaultdict(list)
    for wine in filtered_wines:
        wines_by_category[wine['Категория']].append(wine)
    return wines_by_category


def get_data_file_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="path to file with wine data")
    return parser.parse_args().file_path


if __name__ == '__main__':
    data_file_path = get_data_file_path()
    wines_by_category = get_wines(data_file_path)
    wine_store_age = datetime.datetime.today().year - WINE_STORE_BIRTH_YEAR
    template = get_jinja_template(TEMPLATE_NAME)
    rendered_page = template.render(
        wine_items=wines_by_category,
        wine_store_age=wine_store_age
    )
    with open(RESULT_FILE_NAME, 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
