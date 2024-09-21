import re

from bs4 import BeautifulSoup


async def get_week(html_inp):
    soup = BeautifulSoup(html_inp, features="lxml")
    week = soup.find("h3").text.split("№")[1].split()[0]
    return week


async def get_lesson_id(html_inp):
    soup = BeautifulSoup(html_inp, features="lxml")
    ids = tuple(map(lambda x: x["id"][4:], soup.find_all("span", {"id": re.compile(r"knop+")})))
    return ids
