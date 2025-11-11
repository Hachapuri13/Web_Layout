from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import datetime
import pandas


def get_year_declination(year):
    exceptions = [11, 12, 13, 14]
    declinations = {
        "год": [1],
        "года": [2, 3, 4],
    }
    if len(str(year))>=2 and year%100 in exceptions:
        return "лет"
    elif year%10 in declinations["год"]:
        return "год"
    elif year%10 in declinations["года"]:
        return "года"
    else:
        return "лет"


def main():
    excel_data_df = pandas.read_excel('wine3.xlsx', keep_default_na=False)

    now = datetime.datetime.now()
    now_year = now.year
    foundation_year = 1920
    existence_age = now_year - foundation_year
    year_declination = get_year_declination(existence_age)

    wines = excel_data_df.to_dict(orient='records')
    wines_by_category = defaultdict(list)
    for row in wines:
        category = row['Категория']
        wines_by_category[category].append(row)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        wines=wines_by_category,
        existence_age=existence_age,
        year_declination=year_declination,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
