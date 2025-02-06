import asyncio
import argparse
import os

from bonchapi import BonchAPI

import dotenv


dotenv.load_dotenv(dotenv_path="./examples/autoclick/.env")


parser = argparse.ArgumentParser(
                    prog="bonchcli",
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('week_offset', nargs="?", type=int, default=0)
args = parser.parse_args()


async def main():
    api = BonchAPI()

    api.cookies = {}

    mail = str(os.environ.get("mail"))
    password = str(os.environ.get("password"))

    await api.login(mail, password) 

    rsp = await api.get_timetable(week_offset=args.week_offset)

    week: list[str] = []
    state = True
    firstly = True
    count = 0

    for lesson in rsp:
        try:
            if week[-1] != lesson.date:
                week.append(lesson.date)
        except IndexError:
            week.append(lesson.date)

    for lesson in rsp:
        if firstly:
            firstly = False
            state = True
        elif lesson.date == week[count]:
            state = False
        else:
            print("╚", "─"*32, sep="")
            state = True
            count += 1

        for arg in lesson:
            if arg == lesson.date and state:
                print("\t", "\x1b[93;1m", arg, "\x1b[0m")
#                 print("\t", arg, "\x1b[0m")
            elif arg == lesson.day and state:
                print("\t", arg, "\n")
            elif arg in (lesson.date, lesson.day) and state == False:
                pass
            elif arg == lesson.number:
                if arg is not None:
                    print("\x1b[93;41m", arg, "\x1b[0m", end='')
                else:
                    print("╔", "─", sep="", end='')
            elif arg == lesson.time:
                if state:
                    end = "─"*12
                else:
                    end = ''
                print("─"*4, "\x1b[93;5m",arg, "\x1b[0m", "─"*4, end, sep="")

            elif arg == lesson.lesson_type:
                if lesson.lesson_type == "Лекция":
                        color = "\x1b[94;5m"
                elif lesson.lesson_type == "Практические занятия":
                        color = "\x1b[92;5m"
                elif lesson.lesson_type == "Лабораторная работа":
                        color = "\x1b[91;5m"
                elif lesson.lesson_type == "Консультация":
                        color = "\x1b[95;5m"
                elif lesson.lesson_type in ("Экзамен", "Зачет"):
                        color = "🕱 \x1b[91;5m"
                else:
                    color = "\x1b[94;5m"
                print("│ ", color, arg, "\x1b[0m", sep="")

            elif arg == lesson.teacher:
                print("│ ", "\x1b[77;1m", arg, "\x1b[0m", sep="")
            else:
                print('│', arg)


    print("╚", "─"*32, sep="")

asyncio.run(main())
