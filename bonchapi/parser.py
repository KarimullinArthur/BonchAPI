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


def get_my_lessons(html_inp):
    soup = BeautifulSoup(html_inp, 'html.parser')
    table = soup.find('table', class_='simple-little-table')
    
    schedule_data = []
    rows = table.find_all('tr')
    
    current_day = None
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 1:
            current_day = cols[0].text.strip()
#             temp = re.compile("([a-zA-Z]+)([0-9]+)")
#             current_day = temp.match(current_day).groups()
        elif len(cols) > 1:
            time = cols[0].text.strip()
            number = cols[0].text.strip().split()[0]
            subject = cols[1].find('b').text.strip()
            lesson_type = cols[1].find('small').text.strip()
            location = cols[3].text.strip()
            teacher = cols[4].text.strip()
    
            schedule_data.append({
#                 'date': current_day,
                'day': current_day,
                'time': time,
                'number': number,
                'subject': subject,
                'lesson_type': lesson_type,
                'location': location,
                'teacher': teacher
            })

    return schedule_data 
    
    
    

from pprint import pprint
with open('../index.html') as file:
    for lesson in get_my_lessons(file):
        pprint(lesson)
        print()
#     for lesson in get_my_lessons(file):
#         print(lesson)
