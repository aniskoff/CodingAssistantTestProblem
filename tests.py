import ast
import unittest

import ast_transformer


class TestAstTransformer(unittest.TestCase):
    def _basic_test(self, source, expected_res):
        tree = ast.parse(source)
        ast_transformer.ConstantOptimizer().generic_visit(tree)
        self.assertEqual(ast.dump(tree), expected_res)

    def test_simple_statement(self):
        source = '1 + 2'
        expected_res = 'Module(body=[Expr(value=Constant(value=3))])'
        self._basic_test(source, expected_res)

        source = '(3 + 4) * a'
        expected_res = "Module(body=[Expr(value=BinOp(left=Constant(value=7)," \
                       " op=Mult(), right=Name(id='a', ctx=Load())))])"
        self._basic_test(source, expected_res)

    def test_complex_statement(self):
        source = '1 + 2 + 3'
        expected_res = 'Module(body=[Expr(value=Constant(value=6))])'
        self._basic_test(source, expected_res)

        source = '13 % 3 + 12 ** 2 - 2 // 1'
        expected_res = 'Module(body=[Expr(value=Constant(value=143))])'
        self._basic_test(source, expected_res)

    def test_several_statements(self):
        source = '1 + 2; 2 + 3; 3 + 4'
        expected_res = 'Module(body=[Expr(value=Constant(value=3)), ' \
                       'Expr(value=Constant(value=5)), Expr(value=Constant(value=7))])'
        self._basic_test(source, expected_res)

    def test_add(self):
        source = '1 + 2'
        expected_res = 'Module(body=[Expr(value=Constant(value=3))])'
        self._basic_test(source, expected_res)

    def test_mul(self):
        source = '2 * 3'
        expected_res = 'Module(body=[Expr(value=Constant(value=6))])'
        self._basic_test(source, expected_res)

    def test_zeros(self):
        source = '1 * x'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = 'x * 1'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = '0 * x'
        expected_res = 'Module(body=[Expr(value=Constant(value=0))])'
        self._basic_test(source, expected_res)

        source = 'x * 0'
        expected_res = 'Module(body=[Expr(value=Constant(value=0))])'
        self._basic_test(source, expected_res)

        source = '0 + x'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = 'x + 0'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

    def test_bit_shifts(self):
        source = 'x << 0'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = 'x >> 0'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = '0 << x'
        expected_res = "Module(body=[Expr(value=BinOp(left=Num(n=0)," \
                       " op=LShift(), right=Name(id='x', ctx=Load())))])"
        self._basic_test(source, expected_res)

    def test_pow(self):
        source = 'x ** 1'
        expected_res = "Module(body=[Expr(value=Name(id='x', ctx=Load()))])"
        self._basic_test(source, expected_res)

        source = 'x ** 2'
        expected_res = "Module(body=[Expr(value=BinOp(left=Name(id='x'," \
                       " ctx=Load()), op=Pow(), right=Num(n=2)))])"
        self._basic_test(source, expected_res)

        source = '1 ** x'
        expected_res = 'Module(body=[Expr(value=Constant(value=1))])'
        self._basic_test(source, expected_res)

        source = '2 ** 3'
        expected_res = 'Module(body=[Expr(value=Constant(value=8))])'
        self._basic_test(source, expected_res)

    def test_simple_string(self):
        source = '"Hello " + "World!"'
        expected_res = "Module(body=[Expr(value=Constant(value='Hello World!'))])"
        self._basic_test(source, expected_res)

    def test_complex_string(self):
        source = '2 * ("Bony" + 3 * "And" + "Klaid" )'
        expected_res = "Module(body=[Expr(value=Constant(value='BonyAndAndAndKlaidBonyAndAndAndKlaid'))])"
        self._basic_test(source, expected_res)


if __name__ == '__main__':
    unittest.main()

