from bs4 import BeautifulSoup, element
from datetime import date
from uuid import uuid4
import csv
import html
import json
import os
import requests
import sys


def replace_common_tags(data):
    result = data
    result = result.replace("<br/>", " ")
    result = result.replace("<b>", " ").replace("</b>", " ")
    result = result.replace("<strong>", " ").replace("</strong>", " ")
    result = result.replace("<em>", " ").replace("</em>", " ")
    result = result.replace("<em>", " ").replace("</em>", " ")
    result = result.replace("  ", " ")
    result = result.strip()
    return result


def access_language(key, lang):
    return u"{0}".format(lang[key])


# i18n
folder = "i18n"
en_file = open(os.path.join(folder, "en.json"))
es_file = open(os.path.join(folder, "es.json"))
en = json.load(en_file)
es = json.load(es_file)
en_file.close()
es_file.close()
language = en

try:
    if sys.argv[1] == "en":
        language = en
    elif sys.argv[1] == "es":
        language = es
except IndexError:
    language = en

# output
output_path = "output"
today = str(date.today()).replace("-", "")

# input
url = input(access_language("question", language))
while not url:
    url = input(access_language("question", language))

if url == ":q":
    sys.exit()
response = requests.get(url)

# soup
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

try:
    os.mkdir(output_path)
except:
    pass

for index, table in enumerate(tables):
    filename = os.path.join(
        output_path, "{1}-{2}.csv".format(output_path, today, str(uuid4().hex))
    )
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quotechar='"')
        for table_row in table.children:
            data = []
            if type(table_row) is element.Tag:
                for row_data in table_row.children:
                    if type(row_data) is element.Tag:
                        data_str = replace_common_tags(str(row_data.contents[0]))
                        data.append(html.unescape(data_str))
            writer.writerow(data)
    print(access_language("new_file_created", language) + ": " + filename)
