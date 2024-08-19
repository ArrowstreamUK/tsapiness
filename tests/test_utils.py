# tests/test_utils.py
import unittest
from tsapiness.utils import parse, flatten_variable, add
from tsapiness.tsapi import Label, Variable


class TestUtils(unittest.TestCase):

    def test_add(self):
        d = {}
        label = 'test'
        obj = Label(text='Test Label')
        result = add(d, label, obj, apply_to_tsapi=True)
        self.assertEqual(result['test']['text'], 'Test Label')

    def test_parse(self):
        list_to_parse = [{'text': 'Label 1'}, {'text': 'Label 2'}]
        result = parse(list_to_parse, Label)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, 'Label 1')
        self.assertEqual(result[1].text, 'Label 2')

    def flatten_variable_with_looped_and_values(self):
        variable = Variable(variableId='var1', name='Variable 1',
                            values=[{'valueId': 'val1', 'code': '1',
                                     'label': {'text': 'Value 1'}}],
                            loopedVariables=[{'variableId': 'var2',
                                              'name': 'Variable 2'}])
        variable_list = []
        result = flatten_variable(variable, variable_list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['variable_id'], 'var1')
        self.assertEqual(result[0]['value_id'], 'val1')

    def flatten_variable_with_values_only(self):
        variable = Variable(variableId='var1', name='Variable 1',
                            values=[{'valueId': 'val1',
                                     'code': '1',
                                     'label': {'text': 'Value 1'}}])
        variable_list = []
        result = flatten_variable(variable, variable_list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['variable_id'], 'var1')
        self.assertEqual(result[0]['value_id'], 'val1')

    def flatten_variable_with_looped_only(self):
        variable = Variable(variableId='var1', name='Variable 1',
                            loopedVariables=[{'variableId': 'var2',
                                              'name': 'Variable 2'}])
        variable_list = []
        result = flatten_variable(variable, variable_list)
        self.assertEqual(len(result), 0)

    def flatten_variable_with_no_values_or_looped(self):
        variable = Variable(variableId='var1', name='Variable 1')
        variable_list = []
        result = flatten_variable(variable, variable_list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['variable_id'], 'var1')

    def flatten_variable_with_other_specify_variables(self):
        variable = Variable(variableId='var1',
                            name='Variable 1',
                            otherSpecifyVariables=[{'variableId': 'var2',
                                                    'name': 'Other Var 1'}])
        variable_list = []
        result = flatten_variable(variable, variable_list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['variable_id'], 'var2')


if __name__ == '__main__':
    unittest.main()
