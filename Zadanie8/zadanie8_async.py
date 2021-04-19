import asyncio
import time


async def warm_water_async() -> None:
    print("Heating water")
    await asyncio.sleep(5)
    print("Water has been heated")


async def chopping_vegetables_async() -> None:
    print("Chopping vegetables")
    await asyncio.sleep(2)
    print("Vegetables has been chopped")


async def main():
    start_time = time.time()

    await asyncio.gather(warm_water_async(),chopping_vegetables_async())

    print(time.time() - start_time, "seconds passed")

if __name__ == "__main__":

    asyncio.run(main())