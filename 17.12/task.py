import random
import aiohttp
import asyncio

BASE  = 'https://httpbin.org/delay/'

async def fetch(url: str, session:aiohttp.ClientSession) -> str:
    #одна задача сходить по урл и дождаться ответа
    async with session.get(url, ssl=False) as response:
       await response.text()
       return url


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        task_to_url = {}


        #А + С создаем 10 задач с разными delay
        for _ in range(10):
            delay = random.randint(1, 10)
            url = f'{BASE}{delay}'

            t = asyncio.create_task(fetch(url, session))
            tasks.append(t)
            task_to_url[t] = url

        pending = set(tasks)
        done_total = set()
        #D: каждые 2 секунды проверяем кто уже завершился
        while pending:
            done, pending = await asyncio.wait(pending, timeout=2)
            #накапливаем завершеное
            done_total |= done

            #печетать по условию
            print('Pending(еще не ответили):')
            for t in pending:
                print(' ', task_to_url[t])

            print('DONE(уже ответили)')
            for t in done_total:
                print(' ', task_to_url[t])

            print('-' * 50 )
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())


