"""
    Title: SIH 2020 Scrapper
    File Name: main.py
    Author: Daljeet Singh Chhabra
    Language: Python
    Date Created: 26-12-2019
    Date Modified: 26-12-2019
    ##########################################################################################################
    # Description:
    #       Main script file for scrapping.
    ##########################################################################################################
"""
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
import mechanize
import csv

csv_columns = ['organization', 'problem_title', 'problem_description', 'category', 'domain_bucket', 'youtube_link',
               'dataset_link', 'ps_number']

# BASE URL
URL = 'https://www.sih.gov.in/sih2020PS?page='

# Empty Data dictionary to hold data
data = {}

# Initializing the browser
br = mechanize.Browser()

# Setting Cookie Jar
cj = LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 '
                  'Firefox/3.0.1')]

br.set_handle_robots(False)

PS = []
pages = []
br.open('https://www.sih.gov.in/sih2020PS')
for link in br.links():
    if link.text.isnumeric():
        pages.append(int(link.text))
total_pages = max(pages)
for page in range(1, total_pages+1):
    res = br.open(URL + str(page))
    soup = BeautifulSoup(res.read())
    table = soup.find("table")

    # Extracting useful information
    i = 0
    trs = table.findAll('tr')
    # print(len(trs))
    for i in range(1, len(trs), 7):
        row = trs[i]
        col = row.findAll('td')
        # print(col)
        if len(col) == 0:
            continue
        # print(i)
        # print(col)

        desc_modal = []
        for des in col[2].findAll('tr'):
            des_col = des.findAll('td')
            desc_modal.append(des_col[0].text)

        organization = col[1].string
        problem_title = col[2].text.split(sep='\n')[0]
        problem_title = problem_title.replace('\n', '')
        problem_title = problem_title.replace('\t', '')
        problem_title = problem_title.strip(' ')
        problem_description = desc_modal[0]
        problem_description = problem_description.replace('\n', '')
        problem_description = problem_description.replace('\t', '')
        problem_description = problem_description.strip(' ')
        category = desc_modal[2]
        domain_bucket = desc_modal[3]
        youtube_link = desc_modal[4]
        youtube_link = youtube_link.replace('\n', '')
        youtube_link = youtube_link.replace('\t', '')
        youtube_link = youtube_link.strip(' ')
        dataset_link = desc_modal[5]
        dataset_link = dataset_link.replace('\n', '')
        dataset_link = dataset_link.replace('\t', '')
        dataset_link = dataset_link.strip(' ')
        ps_number = col[10].string
        data = {
            'organization': organization,
            'problem_title': problem_title,
            'problem_description:': problem_description,
            'category': category,
            'domain_bucket': domain_bucket,
            'youtube_link': youtube_link,
            'dataset_link': dataset_link,
            'ps_number': ps_number
        }
        PS.append(data)
        print(data)

print(PS)
csv_file = "SIH 2020 PS.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        for data in PS:
            writer.writerow(data)
except IOError:
    print("I/O error")
