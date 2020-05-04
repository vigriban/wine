from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

WINE_STORE_BIRTH_DATE = 1920

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

wine_store_age = datetime.datetime.today().year - WINE_STORE_BIRTH_DATE

rendered_page = template.render(
    wine_store_age=wine_store_age
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
