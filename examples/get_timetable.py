import asyncio

from bonchapi import BonchAPI

from bonchapi.schemas import Lesson
from get_token_from_browser import Brow


async def main():
    api = BonchAPI()

***REMOVED***
    browser = Brow()
    setattr(api, "cookies", {}) 
    api.cookies["miden"] = browser.get_token()
#     api.cookies["miden"] = "pn1f3ikp1nha77bneb3ei7k96v"
    
#     print(api.cookies)
    
    rsp = await api.get_timetable()

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
                print("\t", arg)
            elif arg == lesson.day and state:
                print("\t", arg, "\n")
            elif arg in (lesson.date, lesson.day) and state == False:
                pass
            elif arg == lesson.number:
                print("\x1b[93;41m", arg, "\x1b[0m", end='')
            elif arg == lesson.time:
                if state:
                    end = "─"*12
                else:
                    end = ''
                print("─"*4, arg, "─"*4, end, sep="")
            else:
                print('│', arg)

asyncio.run(main())
