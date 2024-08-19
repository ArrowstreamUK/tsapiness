import unittest
from tsapiness.tsapi import (SurveyMetadata,
                             Section, Label, Variable,
                             Language, AltLabel, ValueRange,
                             Value, VariableValues,
                             OtherSpecifyVariable, Hierarchy,
                             ParentDetails, MetaData, VariableData,
                             VariableDataItem, Level,
                             HierarchicalInterview, Interview)


class TestTsapi(unittest.TestCase):

    def test_survey_metadata(self):
        survey = SurveyMetadata(name='Survey 1', title='Test Survey')
        self.assertEqual(survey.name, 'Survey 1')
        self.assertEqual(survey.title, 'Test Survey')

    def test_section(self):
        section = Section(label={'text': 'Section 1'})
        self.assertEqual(section.label.text, 'Section 1')

    def test_label(self):
        label = Label(text='Label 1')
        self.assertEqual(label.text, 'Label 1')

    def test_variable(self):
        variable = Variable(variableId='var1', name='Variable 1')
        self.assertEqual(variable.variableId, 'var1')
        self.assertEqual(variable.name, 'Variable 1')

    def test_language(self):
        language = Language(languageId='en', name='English')
        self.assertEqual(language.languageId, 'en')
        self.assertEqual(language.name, 'English')

    def test_alt_label(self):
        alt_label = AltLabel(mode='interview', text='Alt Label 1')
        self.assertEqual(alt_label.mode, 'interview')
        self.assertEqual(alt_label.text, 'Alt Label 1')

    class ValueRange:
        def __init__(self, **kwargs):
            self.range_from = kwargs['from']
            self.range_to = kwargs['to']

    def test_value_range(self):
        value_range = ValueRange(**{'from': 1, 'to': 100})
        self.assertEqual(value_range.range_from, 1)
        self.assertEqual(value_range.range_to, 100)

    def test_value(self):
        value = Value(valueId='val1', code='1', label={'text': 'Value 1'})
        self.assertEqual(value.valueId, 'val1')
        self.assertEqual(value.code, '1')
        self.assertEqual(value.label.text, 'Value 1')

    def test_variable_values(self):
        variable_values = VariableValues(valueListId='vl1',
                                         values=[
                                             {'valueId': 'val1',
                                              'code': '1',
                                              'label': {'text': 'Value 1'}
                                              }])
        self.assertEqual(variable_values.valueListId, 'vl1')
        self.assertEqual(variable_values.values[0].valueId, 'val1')

    def test_other_specify_variable(self):
        osv = OtherSpecifyVariable(parentValueId='pv1',
                                   variableId='var1',
                                   name='Other Specify Variable 1')
        self.assertEqual(osv.parentValueId, 'pv1')
        self.assertEqual(osv.variableId, 'var1')
        self.assertEqual(osv.name, 'Other Specify Variable 1')

    def test_hierarchy(self):
        hierarchy = Hierarchy(hierarchyId='h1')
        self.assertEqual(hierarchy.hierarchyId, 'h1')

    def test_parent_details(self):
        parent_details = ParentDetails(level='1', linkVar='lv1', ordered=True)
        self.assertEqual(parent_details.level, '1')
        self.assertEqual(parent_details.link_var, 'lv1')
        self.assertTrue(parent_details.ordered)

    def test_metadata(self):
        metadata = MetaData(name='Metadata 1', title='Test Metadata')
        self.assertEqual(metadata.name, 'Metadata 1')
        self.assertEqual(metadata.title, 'Test Metadata')

    def test_variable_data(self):
        variable_data = VariableData(variableId='var1')
        self.assertEqual(variable_data.variableId, 'var1')

    def test_variable_data_item(self):
        variable_data_item = VariableDataItem(value='1', state='complete')
        self.assertEqual(variable_data_item.value, '1')
        self.assertEqual(variable_data_item.state, 'complete')

    def test_level(self):
        level = Level(levelId='l1')
        self.assertEqual(level.levelId, 'l1')

    def test_hierarchical_interview(self):
        hierarchical_interview = HierarchicalInterview(level={'levelId': 'l1'},
                                                       interviewId='int1',
                                                       date='2023-10-01')
        self.assertEqual(hierarchical_interview.level.levelId, 'l1')
        self.assertEqual(hierarchical_interview.interviewId, 'int1')
        self.assertEqual(hierarchical_interview.date, '2023-10-01')

    def test_interview(self):
        interview = Interview(interviewId='int1', date='2023-10-01')
        self.assertEqual(interview.interviewId, 'int1')
        self.assertEqual(interview.date, '2023-10-01')


if __name__ == '__main__':
    unittest.main()
