class Node:
    def __init__(self, type):
        self.type = type
        self.children = []

    def __str__(self):
        return str(self.type)

    def __add__(self, other):
        self.children.append(other)

        return self

    def __len__(self):
        return len(self.children)
