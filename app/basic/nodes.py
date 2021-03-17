class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"


class BinOpNode:
    def __init__(self, token, left, rigth):
        self.token = token
        self.left = left
        self.rigth = rigth

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.rigth})"


class UnaryOpNode:
    def __init__(self, token, node):
        self.token = token
        self.node = node

    def __repr__(self):
        return f"({self.token}, {self.node})"
