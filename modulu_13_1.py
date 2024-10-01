from time import sleep
import asyncio


async def start_strongman(name, power, balls_quantity=5):
    try:
        print(f'Силач {name} начал соревнования.')
        for i in range(1, balls_quantity + 1):
            await asyncio.sleep(1 / power)
            print(f'Силач {name} поднял шар номер {i}.')
        print(f'Силач {name} закончил соревнования.')
    except ZeroDivisionError as exc:
        print(f'Силач {name} вышел из турнира. Подъёмная мощность силача не может быть равна нулю. '
              f'\n(Информация для организаторов: {exc}.)')


async def start_tournament():
    print('Старт соревнований.')
    task_1 = asyncio.create_task(start_strongman('Geracl', 12))
    task_2 = asyncio.create_task(start_strongman('Goliaf', 1))
    task_3 = asyncio.create_task(start_strongman('Ilya_Muromets', 7))
    await task_1
    await task_2
    await task_3
    print('Соревнования закончились.')


asyncio.run(start_tournament())
