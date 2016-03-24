import pytest
from WsModule.WsPyModule import ClassExample # for ClassExample


class TestCase:
    """


    """
    tol = 1e-6
    first = 23.4857
    second = 3.4756
    my_list = [6, 7, 8, 9]
    expected_result = 6 + 7 + 8 + 9
    example_object = ClassExample(my_list)


    def testProduct(self):
        result = ClassExample.product(self.first, self.second)
        assert abs(result - (self.first * self.second)) < self.tol

    def testSumListValues(self):
        assert abs(self.expected_result - self.example_object.sumListValues()) < self.tol
