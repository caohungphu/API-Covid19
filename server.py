import os
import json
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ.get('PORT', 80))

url = "https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data#covid19-container"

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
        "flag" : "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Globe.svg/15px-Globe.svg.png",
        "location" : "Worldwide",
        "cases" : data_global_info[2].text.replace('\n',''),
        "deaths" : data_global_info[3].text.replace('\n',''),
        "recovered" : data_global_info[4].text.replace('\n','')
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
                "location" : location.text.replace('\n',''),
                "cases" : data[0].text.replace('\n',''),
                "deaths" : data[1].text.replace('\n',''),
                "recovered" : data[2].text.replace('\n','')
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
            _result = ""
            _result += "Status: Cron Success!\n"
            _result += "Json data: https://ncov-api-hp.herokuapp.com/data.json\n"
            _result += "Source: https://github.com/caohungphu/API-Covid19\n"
            _result += "Author: Cao Hung Phu\n"
            _result += "Facebook: caohungphuvn\n"
            _result += "Contact: caohungphuvn@gmail.com"
            self.wfile.write(bytes(_result, 'utf-8'))

httpd = HTTPServer(('', port), Serv)
httpd.serve_forever()

