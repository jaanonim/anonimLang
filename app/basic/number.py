from .error import RunTimeError


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def __repr__(self):
        return f"{self.value}"

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end, "Cannot divide by 0", self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

    def powed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
