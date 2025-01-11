import asyncio 
import requests

from bonchapi import BonchAPI


async def main():
    api = BonchAPI()
    await api.login("Karimullinarthur@disroot.org", "***REMOVED***")
    print(api.password)
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Combiner Agent'})
    URL = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie_all.php?schet=205.2425%2F1&type_z=1&faculty=57185&kurs=2&group=56204"
    print(requests.get(URL, cookies=api.cookies, headers=headers).text)
#     async with aiohttp.ClientSession() as session:
#         async with session.get(URL, cookies=api.cookies) as resp:
#             print(await resp.text())



if __name__=='__main__':
    asyncio.run(main())
