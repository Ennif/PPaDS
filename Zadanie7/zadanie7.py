def coroutine():
    while True:
        task_id = (yield)
        print("Called coroutine by task ID: ", task_id)


class Task(object):
    id = 0

    def __init__(self, coroutine):
        Task.id += 1
        self.task_id = Task.id
        self.coroutine = coroutine

    def run_task(self, attr):
        return self.coroutine.send(attr)


if __name__ == "__main__":

    coroutine()
