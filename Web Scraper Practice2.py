import requests
from bs4 import BeautifulSoup
import csv

# .text gets source code
source = requests.get("http://coreyms.com").text

soup = BeautifulSoup(source, "lxml")

csv_file = open("cms_scrape.csv", "w")

csv_writer = csv.writer()
csv_writer.wrtierow(["headline", "summary", "video_link"])


article = soup.find("article")

try:
    headline = article.h2.a.text
    print(headline)

    summary = article.find("div", class_="entry-content").p.text
    print(summary)

    vid_src = article.find("iframe", class_="youtube-player")["src"]
    print(vid_src)

    vid_id = vid_src.split("/")[4].split("?")[0]

    yt_link = f"https://youtube.com/watch?v={vid_id}"
    print(vid_id)

# Use Try-Except blocks to manage errors