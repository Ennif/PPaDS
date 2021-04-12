def coroutine():
    while True:
        task_id = (yield)
        print("Called coroutine by task ID: ", task_id)

if __name__ == "__main__":

    coroutine()
