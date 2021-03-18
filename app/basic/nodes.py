class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class BinOpNode:
    def __init__(self, token, left, rigth):
        self.token = token
        self.left = left
        self.rigth = rigth

        self.pos_start = self.left.pos_start
        self.pos_end = self.rigth.pos_end

    def __repr__(self):
        return f"({self.left}, {self.token}, {self.rigth})"


class UnaryOpNode:
    def __init__(self, token, node):
        self.token = token
        self.node = node

        self.pos_start = self.token.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.token}, {self.node})"
