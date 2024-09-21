# BonchAPI

> В будущем, надеюсь *полный* апи клиент для ЛК Бонча
---

## Установка

#### PyPI
`pip install bonchapi`

## Описание
Тестовая сборка асинхронного API клиента личного кабинета [lk.sut.ru](https::/lk.sut.ru)

### [Пример использования](./examples/autoclick/main.py)
```python
import asyncio
from bonchapi import BonchAPI

async def main():
    api = BonchAPI()
    await api.login("YourMail", "YourPassword")
    await api.click_start_lesson() # автокликалка на парах

asyncio.run(main())
```
