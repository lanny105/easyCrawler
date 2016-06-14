__author__ = 'apple'
import re
import urllib2
from bs4 import BeautifulSoup


def getHtml(url):
    page = urllib2.urlopen(url,timeout=10000)
    html = page.read()
    return html

def getContent(html):
    soup = BeautifulSoup(html, "html.parser")
    # soup = BeautifulSoup(html_doc)
    tag = soup.find_all('table')[2]
    URLlist = []
    for tr in tag.find_all('tr'):
        URLlist.append(base + tr.a['href'])

    # for column in soup.find_all('TR')
    return URLlist




base = "http://animecons.com/"
url = "http://animecons.com/events/calendar.shtml/001800799"
html = getHtml(url)
URLlist = getContent(html)

