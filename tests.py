import ast
import unittest

import ast_transformer


class TestAstTransformer(unittest.TestCase):
    def _basic_test(self, source, result):
        tree = ast.parse(source)
        ast_transformer.ConstantOptimizer().generic_visit(tree)
        self.assertEqual(ast.dump(tree), result)

    def test_simple_statement(self):
        source = '1 + 2'
        result = 'Module(body=[Expr(value=Constant(value=3))])'
        self._basic_test(source, result)

    def test_complex_statement(self):
        source = '1 + 2 + 3'
        result = 'Module(body=[Expr(value=Constant(value=6))])'
        self._basic_test(source, result)

    def test_several_statements(self):
        source = '1 + 2; 2 + 3; 3 + 4'
        result = 'Module(body=[Expr(value=Constant(value=3)), Expr(value=Constant(value=5)), Expr(value=Constant(value=7))])'
        self._basic_test(source, result)

    def test_add(self):
        source = '1 + 2'
        result = 'Module(body=[Expr(value=Constant(value=3))])'
        self._basic_test(source, result)

    def test_mul(self):
        source = '2 * 3'
        result = 'Module(body=[Expr(value=Constant(value=6))])'
        self._basic_test(source, result)

    def test_zeros(self):
        source = '1 * x'
        result = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, result)
        source = 'x * 1'
        result = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, result)
        source = '0 * x'
        result = 'Module(body=[Expr(value=Constant(value=0))])'
        self._basic_test(source, result)
        source = 'x * 0'
        result = 'Module(body=[Expr(value=Constant(value=0))])'
        self._basic_test(source, result)
        source = '0 + x'
        result = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, result)
        source = 'x + 0'
        result = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, result)


if __name__ == '__main__':
    unittest.main()

