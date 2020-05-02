import os
import json
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ.get('PORT', 80))

url = "https://en.wikipedia.org/api/rest_v1/page/html/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory"

result_countries = ''

def RunProcess():
    global result_countries
    covid_19_data_main = []
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table",{"class":"wikitable plainrowheaders sortable"})
    rows = table.findAll("tr")
    data_global_info = rows[1].findAll("th")
    data_global_json = {
        "location" : "global",
        "countries " : data_global_info[0].text.replace('\u200d',''),
        "cases" : data_global_info[1].text.replace('\u200d',''),
        "deaths" : data_global_info[2].text.replace('\u200d',''),
        "recovered" : data_global_info[3].text.replace('\u200d','')
    }
    covid_19_data_main.append(data_global_json)
    for row in rows:
        info = row.find_all('th')
        data = row.find_all('td')
        if (data and info):
            flag = info[0].find('img')
            location = info[1].find('a')
            data_json = {
                "flag" : flag['src'].replace('//','https://'),
                "location" : location.text,
                "cases" : data[0].text,
                "deaths" : data[1].text,
                "recovered" : data[2].text
            }
            covid_19_data_main.append(data_json)
    
    result_countries = json.dumps(covid_19_data_main)
    hp_file = open("data.json", "w")
    hp_file.write(result_countries)
    hp_file.close()

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path == '/data.json':
            hp_file_result = open("data.json", "r")
            _result = open(self.path[1:]).read()
            self.wfile.write(bytes(_result, 'utf-8'))
        else:
            RunProcess()
            self.wfile.write(bytes("Cron Success!\nData: https://ncov-api-hp.herokuapp.com/data.json", 'utf-8'))

httpd = HTTPServer(('', port), Serv)
httpd.serve_forever()

