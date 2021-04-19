import asyncio
import time


def warm_water() -> None:
    print("Heating water")
    time.sleep(5)
    print("Water has been heated")


def chopping_vegetables() -> None:
    print("Chopping vegetables")
    time.sleep(2)
    print("Vegetables has been chopped")


def main():
    start_time = time.time()

    warm_water()
    chopping_vegetables()

    print(time.time() - start_time, "seconds passed")

if __name__ == "__main__":

    main()
