import asyncio
import time


def warm_water() -> None:
    print("Heating water")
    time.sleep(5)
    print("Water has been heated")


def main():
    start_time = time.time()

    warm_water()


    print(time.time() - start_time, "seconds passed")

if __name__ == "__main__":

    main()