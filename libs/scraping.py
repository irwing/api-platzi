import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import calendar
import datetime

# get time now
date = datetime.datetime.utcnow()
utc_time = calendar.timegm(date.utctimetuple())

class ScrapingPlatzi():

  def __init__(self, username):
    self.username = username
    self.url = "https://platzi.com/p/" + username
    self.driver = webdriver.Firefox()

  def scraping(self):
    self.driver.get(self.url)
    self.html = self.driver.page_source

    # validate 404 response
    soup = BeautifulSoup(self.html, 'html.parser')
    title = soup.find('title').text
    if(title.find("404") != -1):
      self.driver.quit()
      return 404

    self.driver.quit()

    ''' clear the html '''
    htmlCleared = self.clear_data()
    
    return htmlCleared

  def clear_data(self):

    string = self.html.split("window.data")
    string = string[1].split("window.lang")
    string = string[0]
    string = string.replace(" = {", "")
    string = string.replace("};", "")

    # print(string)

    testString = string.split("\n")

    wantedTags = [
      "careers:",
      "courses:"
    ]
    
    data = {}
    data["username"] = self.username
    data["utctime"] = utc_time

    # loop array
    for indexLineString in range(len(testString)):
      for indexWantedTags in range(len(wantedTags)):
        if(testString[indexLineString].find(wantedTags[indexWantedTags]) != -1):

          label = wantedTags[indexWantedTags]
          stringLine = testString[indexLineString]
          stringLine = stringLine.replace(label, "")
          stringLine = stringLine.strip()

          print(stringLine)
          if(stringLine != "[],"):
            stringLine = stringLine.replace("}],", "}]")
            stringLine = json.loads(stringLine)

            if(label == "careers:"):
              self.clear_careers(stringLine)
            elif (label == "courses:"):
              self.clear_courses(stringLine)

            data[label] = stringLine
          else:
            data[label] = []

    ''' save the html '''
    self.save_output(data)

    return data

  def clear_careers(self, careers):
    for indexCareer in range(len(careers)):
      career = {
        "title": careers[indexCareer]["title"],
        "image": careers[indexCareer]["logo"],
        "color": careers[indexCareer]["color"],
        "approved": careers[indexCareer]["approved"],
        "golden_achievement": careers[indexCareer]["golden_achievement"],
        "diploma_link": careers[indexCareer]["diploma_link"],
      }
      careers[indexCareer] = career
    return careers

  def clear_courses(self, courses):
    for indexCourse in range(len(courses)):
      course = {
        "title": courses[indexCourse]["title"],
        "image": courses[indexCourse]["image"],
        "color": courses[indexCourse]["color"],
        "badge": courses[indexCourse]["badge"],
        "url": courses[indexCourse]["url"],
        "approved": courses[indexCourse]["approved"],
        "diploma_link": courses[indexCourse]["diploma_link"],
      }
      courses[indexCourse] = course
    return courses

  def save_output(self, data):
    with open("outputs/" + self.username + ".json", "w") as outfile:
      json.dump(data, outfile, indent=4)
