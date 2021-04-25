class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class StringNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end


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
        self.pos_end = (self.else_case or self.cases[-1])[0].pos_end


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


class ForNode:
    def __init__(
        self,
        var_name_tok,
        start_value_node,
        end_value_node,
        step_value_node,
        body_node,
        return_null,
    ):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.return_null = return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class WhileNode:
    def __init__(self, condition_node, body_node, return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.return_null = return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


class FuncDefNode:
    def __init__(self, var_name_tok, arg_names_toks, body_node, return_null):
        self.var_name_tok = var_name_tok
        self.arg_names_toks = arg_names_toks
        self.body_node = body_node
        self.return_null = return_null

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_names_toks) > 0:
            self.pos_start = self.arg_names_toks[0].pos_start
        else:
            self.pos_start = self.body_node

        self.pos_end = self.body_node.pos_end


class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
