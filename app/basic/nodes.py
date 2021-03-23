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


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1][0]).pos_end


class VarAccessNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end


class VarAssignNode:
    def __init__(self, token, value):
        self.token = token
        self.value = value

        self.pos_start = self.token.pos_start
        self.pos_end = self.value.pos_end
