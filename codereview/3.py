def merge_lists(list1, list2):
    merged_list = list1 + list2
    return merged_list

class Merger:
    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    def merge(self):
        return merge_lists(self.list1, self.list2)

m = Merger([1, 2, 3], [4, 5, 6])
print(m.merge())
