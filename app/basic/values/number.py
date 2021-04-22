from ..error import RunTimeError
from .value import Value


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end, "Cannot divide by 0", self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def powed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def anded_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value and other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def ored_by(self, other):
        if isinstance(other, Number):
            return (
                Number(int(self.value or other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def is_true(self):
        return self.value != 0

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
