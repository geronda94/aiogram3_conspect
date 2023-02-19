import asyncio

async def some_task(param):
    return param

async def main():
    params = [x for x in range(100_000)]  # набор параметров
    tasks = []
    counter = 0
    for param in params:
        task = asyncio.create_task(some_task(param))
        tasks.append(task)
        counter+=1
        if counter ==2_000:
            results = await asyncio.gather(*tasks)  # выполнение задач
            print(sum(results))
            tasks=[]
            counter=0

asyncio.run(main())