class FirstNonConsecutive:
    def __init__(self, arr):
        assert isinstance(arr, object)
        self.arr = arr

    def find_first_non_consecutive(self):
        for num in range(1, len(self.arr)):
            if self.arr[num] != self.arr[num - 1] + 1:
                return self.arr[num]
        return None

    @staticmethod
    def find_first_non_consecutive(arr):
        for num in range(1, len(arr)):
            if arr[num] != arr[num - 1] + 1:
                return arr[num]
        return None

    @classmethod
    def find_first_non_consecutive(cls, arr):
        for num in range(1, len(arr)):
            if arr[num] != arr[num - 1] + 1:
                return arr[num]
        return None


class FindShortString:
    def find_short(self, string):
        self.string = string
        self.words = string.split()
        self.sort = sorted(self.words, key=len)
        if len(self.sort) == 1:
            self.short = "".join(self.sort)
            return len(self.short)
        else:
            for word in self.sort:
                self.short = len(self.sort[0])
                if len(word) <= self.short:
                    self.short = word
        return self.short


class Strlen:
    @staticmethod
    def strlen(string):
        i = 0
        for char in string:
            i += 1
        return i


class FindMaxAndMin:
    def __init__(self, arr):
        self.arr = arr
        self.min_value = None
        self.max_value = None
        self.find_max_and_min()

    def find_max_and_min(self):
        if not self.arr:
            # Handle empty array
            return

        self.max_value = self.arr[0]
        self.min_value = self.arr[0]

        for num in self.arr:
            if num > self.max_value:
                self.max_value = num
            elif num < self.min_value:
                self.min_value = num
                
    def get_max(self):
        return self.max_value

    def get_min(self):
        return self.min_value
