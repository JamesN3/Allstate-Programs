import requests
from bs4 import BeautifulSoup

with open("simple.html") as html_file:
    soup = BeautifulSoup(html_file, "lxml")

match = soup.title.text
# .text gets only text and removes tag
# Only gets first tag on page
print(match)

article = soup.find("div", class_="article")
print(article)

headline = article.h2.a.text
print(headline)
# Grabs header2, a tag, then text from html in article

summary = article.p.text
print(summary)

# Returns list of all
article1 = soup.find_all("div", class_="article")
print(article1)
