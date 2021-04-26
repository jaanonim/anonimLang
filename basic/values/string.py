from ..error import RunTimeError
from .number import Number
from .value import Value


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            print(self.pos_start, other.pos_end)
            return None, Value.illegal_operation(other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        else:
            return None, Value.illegal_operation(other)

    def is_true(self):
        return len(self.value) > 0
