import aiohttp

from . import parser


class AuthError(ValueError):
    default_message = "invalid username or password"

    def __init__(self, message=None):
        super().__init__(message or self.default_message)


class BonchAPI:
    @staticmethod
    async def get_token() -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://lk.sut.ru/cabinet/?") as resp:
                token = (
                    str(resp.cookies.get("miden"))
                    .split(":")[1]
                    .split("=")[1]
                    .split(";")[0]
                )
                return token

    async def login(self, mail: str, password: str) -> bool:
        URL = "https://lk.sut.ru/cabinet/lib/autentificationok.php"

        token = await self.get_token()
        self.mail = mail
        self.password = password
        self.cookies = {"miden": token}
        payload = {"users": mail, "parole": password}

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, cookies=self.cookies, data=payload) as resp:
                if await resp.text() == "1":
                    return True
                else:
                    raise AuthError

    async def get_raw_timetable(self):
        URL = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php"

        async with aiohttp.ClientSession() as session:
            async with session.post(URL, cookies=self.cookies) as resp:
                bonch_acess_error_msg = "У Вас нет прав доступа. Или необходимо перезагрузить приложение.."
                if await resp.text() == bonch_acess_error_msg:
                    await self.login(self.mail, self.password)
                    await self.get_raw_timetable()
                return await resp.text()

    async def get_timetable(self):
        return await parser.get_my_lessons(await self.get_raw_timetable())

    async def click_start_lesson(self):
        URL = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php"

        timetable = await self.get_raw_timetable()
        week = await parser.get_week(timetable)

        for lesson_id in await parser.get_lesson_id(timetable):
            data = {"open": 1, "rasp": lesson_id, "week": week}

            async with aiohttp.ClientSession() as session:
                async with session.post(URL, cookies=self.cookies, params=data) as resp:
                    await resp.text()
