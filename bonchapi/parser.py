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


async def get_my_lessons(html_inp) -> list[dict]:
    soup = BeautifulSoup(html_inp, "html.parser")
    table = soup.find("table", class_="simple-little-table")

    schedule_data = []
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 1:
            current_day = cols[0].text.strip()
        elif len(cols) > 1:
            time = cols[0].text.strip().split()[-1]
            number = cols[0].text.strip().split()[0]
            subject = cols[1].find("b").text.strip()
            lesson_type = cols[1].find("small").text.strip()
            location = cols[3].text.strip()
            teacher = cols[4].text.strip()

            # Динамит вне времени...
            if time[0] == "(":
                time = cols[0].text.strip().split()[-1][1:-1]
            
            # Нажал кнопку начать занятие..
            if "началось" in lesson_type.split():
                lesson_type = " ".join(
                    lesson_type.split()[: lesson_type.split().index("началось") - 1]
                )

            for char in current_day:
                if char in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
                    date = current_day[current_day.index(char) :]
                    current_day = current_day[: current_day.index(char)]
                    break

            schedule_data.append(
                {
                    "date": date,
                    "day": current_day,
                    "time": time,
                    "number": number,
                    "subject": subject,
                    "lesson_type": lesson_type,
                    "location": location,
                    "teacher": teacher,
                }
            )

    return schedule_data
