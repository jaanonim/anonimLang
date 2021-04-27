from .symbols import SymbolTable


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

    def generate_new_context(self, name, pos_start=None):
        new_context = Context(name, self, pos_start or self.parent_entry_pos)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
