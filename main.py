__author__ = 'apple'

import json
import csv
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
    eventType = "Anime"

    for url in URLlist:
        dup = False
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

        registerLink = ""
        if soup.find_all("a", text="Register Now")!= []:
            registerLink = soup.find_all("a", text="Register Now")[0]['href']


        advanceRates = ""
        if soup.find_all("b", text="Advance Rates:")!=[]:
            a = soup.find_all("b", text="Advance Rates:")[0].find_parent()
            for e in a.find_all('br'):
                e.extract()

            b = a.contents[1:]
            advanceRates = '\n'.join(b)
            advanceRates.strip()

        atDoorRates = ""
        if soup.find_all("b", text="At-Door Rates:")!=[]:
            a = soup.find_all("b", text="At-Door Rates:")[0].find_parent()
            for e in a.find_all('br'):
                e.extract()

            b = a.contents[1:]
            atDoorRates = '\n'.join(b)
            advanceRates.strip()


        if record.keys() == []:
            record[name.lower()] = eventStartDate
        else :

            for key in record.keys():
                if (key.find(name.lower()) != -1 or name.lower().find(key)!= -1) and record[key] == eventStartDate:
                    print "duplicates!", name, eventStartDate
                    dup = True
                    break

        if dup:
            continue

        record[name.lower()] = eventStartDate
        writer.writerow([name,eventVenue,eventCity,eventState,country,eventStartDate,eventEndDate,latitude,longitude,advanceRates,atDoorRates,link\
                         ,registerLink,eventDescription,eventType])


def getURL2(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find('div', 'list_cons')
    URLlist = []
    for a in tag.find_all('a'):
        URLlist.append(base2 + a['href'])
        print base2 + a['href']

    return URLlist


def getContent2(URLlist):
    eventType = "Comic"

    for url in URLlist:
        dup = False
        html = getHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.find('div',id='con')
        name = tag.h1.contents[0].strip()

        date = tag.find('div',id='dates')

        eventStartDate = date.find('meta',itemprop="startDate")["content"].strip()
        eventEndDate = date.find('meta',itemprop="endDate")["content"].strip()

        tag2 = soup.find('div',id='con_details')

        eventDescription = ""
        if tag2.find_all('div',"clear")!= []:
            for x in tag2.find_all('div',"clear"):
                if x.text!='':
                    eventDescription = x.text.strip()
                    break

        tag3 = soup.find('div',id='complete_location')


        link = ""
        registerLink = ""
        advanceRates = ""
        atDoorRates = ""
        latitude = ""
        longitude = ""
        eventVenue = ""
        eventCity = ""
        eventState = ""


        if tag3.find_all('div',itemprop="name")!=[]:
            eventVenue = tag3.find('div',itemprop="name").text.strip()

        if tag3.find_all('b',itemprop="addressLocality")!=[]:
            eventCity = tag3.find_all('b',itemprop="addressLocality")[0].text.strip()

        if tag3.find_all('b',itemprop="addressRegion")!=[]:
            eventState = tag3.find_all('b',itemprop="addressRegion")[0].text.strip()
        country = "USA"

        if soup.find_all("a", text="Official Website")!=[]:
            link = soup.find_all("a", text="Official Website")[0]['href']

        if record.keys() == []:
            record[name.lower()] = eventStartDate
        else :

            for key in record.keys():
                if (key.find(name.lower()) != -1 or name.lower().find(key)!= -1) and record[key] == eventStartDate:
                    print "duplicates!", name, eventStartDate
                    dup = True
                    break

        if dup:
            continue

        record[name.lower()] = eventStartDate
        writer.writerow([name,eventVenue,eventCity,eventState,country,eventStartDate,eventEndDate,latitude,longitude,advanceRates,atDoorRates,link\
                         ,registerLink,eventDescription,eventType])




def fbget(type):

    fbURL = 'https://graph.facebook.com/v2.6/search?q=' + type + '&type=event&center=34.0225483%2C-118.2832203&distance=100&access_token=EAACEdEose0cBAFyF4K09MRcsZAylGgkSwQiFlDSHp4dQqjFTtVTyC6R6StGKpID72shR3q5sOFajphpTA4KuO7xn2IARxjJtqnHdeX2e1WXlyYFHmwFXoEz41sJJZB3UWUZAqb6heoZCQMkE48ZAsiBfIFSQPkRkyBXKZAAcYp6AZDZD'
    html3 = getHtml(fbURL)
    hjson = json.loads(html3)


    while 'data' in hjson.keys():
        for x in hjson['data']:

            dup = False

            if "place" not in x.keys() or "location" not in x["place"].keys() or "country" not in x["place"]["location"].keys():
                continue

            if x["place"]["location"]["country"] != "United States" and x["place"]["location"]["country"] != "Canada":
                continue



            name = ""
            eventVenue = ""
            eventCity = ""
            eventState = ""
            country = ""
            eventStartDate = ""
            eventEndDate = ""
            latitude = ""
            longitude =""
            advanceRates = ""
            atDoorRates = ""
            link = ""
            registerLink = ""
            eventDescription = ""
            eventType = type

            if "name" in x.keys():
                name = x["name"]

            eventVenue = x["place"]["name"]

            if "city" in x["place"]["location"].keys():
                eventCity = x["place"]["location"]["city"]

            if "state" in x["place"]["location"].keys():
                eventState = x["place"]["location"]["state"]

            if x["place"]["location"]["country"] == "United States":
                country = "USA"
            else:
                country = "Canada"

            if "start_time" in x.keys():
                eventStartDate = x["start_time"][:10]

            if "end_time" in x.keys():
                eventEndDate = x["end_time"][:10]

            if "latitude" in x["place"]["location"].keys():
                latitude = x["place"]["location"]["latitude"]

            if "longitude" in x["place"]["location"].keys():
                longitude = x["place"]["location"]["longitude"]

            if "description" in x.keys():
                eventDescription = x["description"]

            if record.keys() == []:
                record[name.lower()] = eventStartDate
            else :

                for key in record.keys():
                    if (key.find(name.lower()) != -1 or name.lower().find(key)!= -1) and record[key] == eventStartDate:
                        print "duplicates!", name, eventStartDate
                        dup = True
                        break

            if dup:
                continue

            record[name.lower()] = eventStartDate
            writer.writerow([name,eventVenue,eventCity,eventState,country,eventStartDate,eventEndDate,latitude,longitude,advanceRates,atDoorRates,link\
                         ,registerLink,eventDescription,eventType])


        if 'paging' in hjson.keys():
            fbURL = hjson['paging']['next']
            html3 = getHtml(fbURL)
            hjson = json.loads(html3)

        else:
            break


writer = csv.writer(file('output.csv', 'w'))
writer.writerow(['name', 'eventVenue', 'eventCity', 'eventState', 'eventCountry', 'eventStartDate', 'eventEndDate', 'latitude', 'longitude', \
        'advanceRates', 'atDoorRates', 'siteURL', 'registerURL', 'description', 'eventType'])


record = {}

base = "http://animecons.com/"
url = "http://animecons.com/events/calendar.shtml/001800799"
html = getHtml(url)
URLlist = getURL(html)
getContent(URLlist)



base2 = "http://www.upcomingcons.com/"
url2 = "http://www.upcomingcons.com/comic-conventions"
html2 = getHtml(url2)
URLlist2 = getURL2(html2)
getContent2(URLlist2)


fbget("Anime")
fbget("Comic")


print record