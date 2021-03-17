class Position:
    def __init__(self, id, ln, col, fn, ftxt):
        self.id = id
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, char=None):
        self.id += 1
        self.col += 1
        if char == "\n":
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.id, self.ln, self.col, self.fn, self.ftxt)
