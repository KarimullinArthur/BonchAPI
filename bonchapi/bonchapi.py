import aiohttp
from typing import List

from . import parser
from . import schemas
from bonchapi import schemas


class AuthError(ValueError):
    default_message = "invalid username or password"

    def __init__(self, message=None):
        super().__init__(message or self.default_message)


class BonchAPI:
    @staticmethod
    async def get_token() -> str:
        URL = "https://lk.sut.ru/cabinet"

        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as resp:
                resp.raise_for_status()
                token = (
                    str(resp.cookies.get("miden"))
                    .split(":")[1]
                    .split("=")[1]
                    .split(";")[0]
                )
                return token

    async def login(self, mail: str, password: str) -> bool:
        AUTH = f"https://lk.sut.ru/cabinet/lib/autentificationok.php?users={mail}&parole={password}"
        CABINET = "https://lk.sut.ru/cabinet/"
        
        self.token = await self.get_token()
        self.mail = mail
        self.password = password
        self.cookies = {"miden": self.token}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(CABINET) as resp:
                resp.raise_for_status()

                self.cookies = resp.cookies
                self.cookies["miden"] = self.token

                async with session.post(AUTH) as resp:
                    resp.raise_for_status()
                    text = await resp.text()
                    if text == '1':
                        async with session.get(CABINET) as resp:
                            return True
                    else:
                        raise AuthError

    async def get_raw_timetable(self, week_number: int = False) -> str:
        URL = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php"
        if week_number:
            URL += f"?week={week_number}"

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, cookies=self.cookies) as resp:
                bonch_acess_error_msg = "У Вас нет прав доступа. Или необходимо перезагрузить приложение.."
                if await resp.text() == bonch_acess_error_msg:
                    await self.login(self.mail, self.password)
                    await self.get_raw_timetable(week_number)
                return await resp.text()

    async def find_first_week_id(self) -> int:
        '''
        Получение ID первой учебной недели в *семестре*
        '''
        MAX_WEEK = 50

        for i in (0,-1,-2,1,2):
            id = MAX_WEEK//2+i
            guess = await parser.get_week(await self.get_raw_timetable(id))
            if guess == 0:
                return id
        return 0
    
    async def get_timetable(self, week_number: int = False, *, week_offset: int = False) -> List[schemas.Lesson]:
        if week_offset:

            if not hasattr(self, "_first_week"):
                self._first_week = await self.find_first_week_id()
                
            current_week = await parser.get_week(await self.get_raw_timetable(week_number))
            desired_week = current_week + week_offset + self._first_week
            return await parser.get_my_lessons(await self.get_raw_timetable(desired_week))

        else:
            return await parser.get_my_lessons(await self.get_raw_timetable(week_number))

    async def click_start_lesson(self):
        URL = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php"

        timetable = await self.get_raw_timetable()
        week = await parser.get_week(timetable)

        for lesson_id in await parser.get_lesson_id(timetable):
            data = {"open": 1, "rasp": lesson_id, "week": week}

            async with aiohttp.ClientSession() as session:
                async with session.post(URL, cookies=self.cookies, params=data) as resp:
                    await resp.text()
