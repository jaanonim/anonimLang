from .strings_with_arrows import string_with_arrows


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_str(self):
        r = f"{self.error_name}: {self.details}\n"
        r += f"In {self.pos_start.fn}, at line {self.pos_start.ln + 1}, char: {self.pos_start.col + 1}"
        r += "\n\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return r


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Char Error", details)


class ExceptedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Excepted Char Error", details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax Error", details)


class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Run Time Error", details)
        self.context = context

    def as_str(self):
        r = self.generate_trace()
        r += f"{self.error_name}: {self.details}\n"
        r += "\n" + string_with_arrows(
            self.pos_start.ftxt, self.pos_start, self.pos_end
        )
        return r

    def generate_trace(self):
        r = ""
        pos = self.pos_start
        con = self.context

        while con:
            r = f"In {pos.fn} in {con.display_name}, at line {pos.ln + 1}, char: {pos.col + 1}\n"
            pos = con.parent_entry_pos
            con = con.parent
        return "Traceback:\n" + r
