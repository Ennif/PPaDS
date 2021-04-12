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


class Scheduler:

    def __init__(self):
        self.last_coroutine = 0
        self.array_of_coroutines = []
        self.number_of_coroutines = 0
        self.index = 1

    def fill_array(self, coroutine):
        new_task = Task(coroutine)
        new_task.run_task(None)
        self.array_of_coroutines.insert(new_task.task_id, new_task)

    def main(self):
        pass


if __name__ == "__main__":

    coroutine()
