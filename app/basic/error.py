class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_str(self):
        r = f"{self.error_name}: {self.details}\n"
        r += f"In {self.pos_start.fn}, at line {self.pos_start.ln + 1}, char: {self.pos_start.col + 1}"
        return r


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Char Error", details)
