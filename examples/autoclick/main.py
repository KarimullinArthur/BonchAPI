import asyncio

from bonchapi import BonchAPI

from config import config


async def main():
    api = BonchAPI()
    await api.login(config.mail, config.password)
    await api.click_start_lesson()


asyncio.run(main())
