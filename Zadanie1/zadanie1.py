import fei.ppds as fp


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end


for _ in range(5):
    shared_object = Shared(1000)
    print(shared_object.array)
