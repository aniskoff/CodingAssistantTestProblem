import ast
import operator


class ConstantOptimizer(ast.NodeTransformer):
    # mapping ast operators to "action" operators
    _ast_op_to_action_op = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.MatMult: operator.matmul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
        ast.FloorDiv: operator.floordiv,
    }

    @staticmethod
    def _common_value_getter(const_like_instance):
        instance_class = const_like_instance.__class__

        if (instance_class is ast.Constant) or (instance_class is ast.NameConstant):
            return const_like_instance.value

        elif instance_class is ast.Num:
            return const_like_instance.n

        elif (instance_class is ast.Str) or (instance_class is ast.Bytes):
            return const_like_instance.s

        else:
            assert False, 'Unexpected behavior!'  # or Exception

    def visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)

        if not isinstance(node, ast.BinOp):
            return node

        left = node.left
        right = node.right
        op = node.op

        const_like_types = (ast.Constant, ast.Num, ast.Str, ast.NameConstant, ast.Bytes)
        if isinstance(left, const_like_types) and isinstance(right, const_like_types):
            left_val = ConstantOptimizer._common_value_getter(left)
            right_val = ConstantOptimizer._common_value_getter(right)
            op_action = self._ast_op_to_action_op[op.__class__]
            return ast.Constant(value=op_action(left_val, right_val))

        # Handles expressions such as:
        # '1 * x' -> 'x',
        # '0 * x' -> '0',
        # '1 * (2 + x)' -> (2 + x),
        # '1 ** x' -> 1,
        # ...
        elif isinstance(left, const_like_types):

            left_val = ConstantOptimizer._common_value_getter(left)

            if left_val == 0:
                if isinstance(op, ast.Mult) or isinstance(op, ast.Pow):
                    return ast.Constant(value=0)

                elif isinstance(op, ast.Add):
                    return right

                else:
                    return node

            elif left_val == 1:
                if isinstance(op, ast.Mult):
                    return right

                elif isinstance(op, ast.Pow):
                    return ast.Constant(value=1)

                else:
                    return node

            else:
                return node

        # The same as previous one,
        # but with 1 or 0 on the right side of the expression
        # Handles expressions such as:
        # 'x * 1' -> 'x',
        # 'x * 0' -> '0',
        # '(2 + x) * 1' -> '(2 + x)',
        # 'x ** 1' -> 'x',
        # 'x << 0' -> 'x',
        # 'x >> 0' -> 'x'
        # ...
        elif isinstance(right, const_like_types):
            right_val = ConstantOptimizer._common_value_getter(right)

            if right_val == 0:
                if isinstance(op, ast.Mult):
                    return ast.Constant(value=0)

                elif isinstance(op, (ast.Add, ast.LShift, ast.RShift)):
                    return left

                elif isinstance(op, ast.Pow):
                    return ast.Constant(value=1)

                else:
                    return node

            elif right_val == 1:
                if isinstance(op, (ast.Mult, ast.Pow)):
                    return left

                elif isinstance(op, ast.Pow):
                    return ast.Constant(value=1)

                else:
                    return node

            else:
                return node

        else:

            return node

