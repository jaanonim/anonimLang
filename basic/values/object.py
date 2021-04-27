from .value import Value


class Object(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f"<object: {self.value.display_name}>"

    def copy(self):
        copy = Object(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
