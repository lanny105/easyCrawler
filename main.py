__author__ = 'apple'
import re
import urllib2
from bs4 import BeautifulSoup


def getHtml(url):
    page = urllib2.urlopen(url,timeout=10000)
    html = page.read()
    return html

def getURL(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find_all('table')[2]
    URLlist = []
    for tr in tag.find_all('tr'):
        if tr.find_all('',text="Cancelled"):
            continue
        URLlist.append(base + tr.a['href'])

    return URLlist

def getContent(URLlist):
    for url in URLlist[:]:
        html = getHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find_all('table')[1]
        date = tag.find_all('time')
        eventStartDate = date[0]["datetime"].strip()
        eventEndDate = date[1]["datetime"].strip()
        link = tag.h1.a["href"].strip()
        name = tag.h1.a.contents[0].strip()
        eventVenue = tag.find_all('span',itemprop="name")[0].contents[0].strip()
        latitude = tag.find_all('meta',itemprop="latitude")[0]["content"].strip()
        longitude = tag.find_all('meta',itemprop="longitude")[0]["content"].strip()

        addr = tag.find_all("div","address")[0].a

        eventCity = addr.find_all('span',itemprop="addressLocality")[0].contents[0].strip()
        eventState = addr.find_all('span',itemprop="addressRegion")[0].contents[0].strip()
        country = tag.find_all('meta',itemprop="addressCountry")[0]["content"].strip()


        eventDescription = ""
        if soup.find_all('span',itemprop="description")!= []:
            eventDescription = soup.find_all('span',itemprop="description")[0].contents[0].strip()

        rigisterLink = ""
        if soup.find_all("a", text="Register Now")!= []:
            rigisterLink = soup.find_all("a", text="Register Now")[0]['href']


        advanceRates = ""
        if soup.find_all("b", text="Advance Rates:")!=[]:
            advanceRates = ' '.join([str(w) if w != "<br/>" else " " for w in soup.find_all("b", text="Advance Rates:")[0].find_parent().contents][1:])

        atDoorRates = ""
        if soup.find_all("b", text="At-Door Rates:")!=[]:
            advanceRates = soup.find_all("b", text="At-Door Rates:")[0].find_parent().get_text().split('\n')

        print [eventStartDate,eventEndDate,link,name,eventVenue,latitude,longitude,eventCity,eventState,country,eventDescription,rigisterLink,eventType]



eventType = "Anime"
base = "http://animecons.com/"
url = "http://animecons.com/events/calendar.shtml/001800799"
html = getHtml(url)
URLlist = getURL(html)
getContent(URLlist)
