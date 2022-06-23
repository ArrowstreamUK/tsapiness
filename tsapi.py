from enum import Enum
import requests
import json

SERVER = ''


class VariableType(Enum):
    SINGLE = 'Single'
    MULTI = 'Multiple'
    QUANTITY = 'Quantity'
    CHARACTER = 'Character'
    LOGICAL = 'Logical'
    DATE = 'Date'
    TIME = 'Time'


class AltLabelMode(Enum):
    INTERVIEW = 1
    ANALYSIS = 2


def parse(list_to_parse, obj):
    list_to_return = []
    if list_to_parse is not None:
        for list_item in list_to_parse:
            list_item_obj = obj(**list_item)
            list_to_return.append(list_item_obj)
    return list_to_return


def flatten_variable(variable, variable_list):
    if len(variable.looped_variables) > 0 and len(variable.values) > 0:
        for value in variable.values:
            _a = variable.to_dict()
            _a.update(value.to_dict())
            variable_list.append(_a)
        for loop_variable in variable.looped_variable_values:
            flatten_variable(variable=loop_variable,
                             variable_list=variable_list)
    elif len(variable.looped_variables) == 0 and len(variable.values) > 0:
        _a = variable.to_dict()
        for value in variable.values:
            _a = variable.to_dict()
            _a.update(value.to_dict())
            variable_list.append(_a)
    elif len(variable.looped_variables) > 0 and len(variable.values) == 0:
        # check if this is valid
        pass

    elif len(variable.looped_variables) == 0 and len(variable.values) == 0:
        _a = variable.to_dict()
        variable_list.append(_a)
    else:
        _a = variable.to_dict()
        variable_list.append(_a)
    if len(variable.otherSpecifyVariables) > 0:
        for osv in variable.otherSpecifyVariables:
            flatten_variable(variable=osv, variable_list=variable_list)

    return variable_list


class Survey:
    def __init__(self, hierarchies=None, name="", title="", interviewCount=0,
                 languages=None, notAsked="", noAnswer="", variables=None,
                 sections=None):
        self._hierarchies = hierarchies
        self.hierarchies = parse(self._hierarchies, Hierarchy)
        self.name = name
        self.title = title
        self.interview_count = interviewCount
        self.not_asked = notAsked
        self.no_answer = noAnswer
        self._variables = variables
        self.variables = parse(self._variables, Variable)
        self._sections = sections
        self.sections = parse(self._sections, Section)
        self._languages = languages
        self.languages = parse(self._languages, Language)

    def __str__(self):
        return f'Name: {self.name}, Title {self.title}'

    def __repr__(self):
        return f'Survey({self.name})'


class Section:
    def __init__(self, label, variables):
        self._label = label
        self.label = Label(**label)
        self._variables = variables
        self.sections = ""
        self.variables = parse(self._variables, Variable)

    def __str__(self):
        return f'{self.label}'

    def __repr__(self):
        return f'{self.label}'


class Label:
    def __init__(self, text, altLabels=None):

        self.text = text
        self._alt_label = altLabels
        self.alt_labels = parse(self._alt_label, AltLabel)

    def __str__(self):
        return self.text

    @property
    def label_analysis(self) -> str:
        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == AltLabelMode.ANALYSIS:
                    alt_text = alts.text
                    return alt_text
        return alt_text

    @property
    def label_interview(self) -> str:
        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == AltLabelMode.INTERVIEW:
                    return alts.text
        return alt_text


class Variable:
    def __init__(self,
                 ordinal=0,
                 label=None,
                 name="",
                 ident="",
                 type="",
                 values=None,
                 use="",
                 maxResponses=0,
                 loopedVariables=None,
                 otherSpecifyVariables=None):

        # if otherSpecifyVariables is None:
        #     otherSpecifyVariables = []
        self._otherSpecifyVariables = otherSpecifyVariables
        self.otherSpecifyVariables = parse(self._otherSpecifyVariables,
                                           OtherSpecifyVariable)

        self.ident: str = ident
        self.ordinal: int = ordinal
        self._type: str = type
        self.name: str = name
        self._label: dict = label
        self.label: Label = Label(**label)
        self.use: str = use
        self.maxResponses: int = maxResponses

        if values is None:
            values = {}
        self._variable_values = values
        self.variable_values = VariableValues(**values)

        self._loopedVariables = loopedVariables
        self.looped_variables = parse(self._loopedVariables, Variable)

    @property
    def looped_variable_values(self):
        looped_variable_value_list = []
        if len(self.values) == 0 | len(self.looped_variables) == 0:
            return looped_variable_value_list

        for value in self.values:
            for l_v in self.looped_variables:
                loop_ref = LoopRef(self.ident, value.ident)
                l_v = LoopedVariable(ordinal=l_v.ordinal,
                                     label=l_v._label,
                                     name=l_v.name,
                                     ident=l_v.ident,
                                     type=l_v._type,
                                     values=l_v._variable_values,
                                     use=l_v.use,
                                     maxResponses=l_v.maxResponses,
                                     loopedVariables=l_v._loopedVariables,
                                     otherSpecifyVariables=l_v._otherSpecifyVariables,
                                     loop_ref=loop_ref
                                     )
                looped_variable_value_list.append(l_v)
        return looped_variable_value_list

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    @property
    def type(self):
        return VariableType(self._type)

    @property
    def alt_labels(self):
        return self.label.alt_labels

    @property
    def label_text(self):
        return self.label.text

    @property
    def values(self):
        return self.variable_values.values

    @property
    def label_interview(self):
        return self.label.label_interview

    @property
    def label_analysis(self):
        return self.label.label_analysis

    @property
    def range_from(self):
        _r = ""
        if self.variable_values._range:
            _r = self.variable_values.range.range_from
        return _r

    @property
    def range_to(self):
        _r = ""
        if self.variable_values._range:
            _r = self.variable_values.range.range_to
        return _r

    def range(self):
        return self.variable_values.range

    def to_dict(self):
        _dict = {
            'var_name': self.name,
            'variable_name': self.name,
            'variable_ident': self.ident,
            'variable_label': self.label_text,
            'variable_type': self.type.name,
            'variable_interview_label': self.label_interview,
            'variable_analysis_label': self.label_analysis,
        }
        if self.range:
            _dict['variable_range_from'] = self.range_from
            _dict['variable_range_to'] = self.range_to
        return _dict


class Language:
    def __init__(self, ident="", name="", subLanguages=None):
        if subLanguages is None:
            subLanguages = []
        self.ident = ident
        self.name = name
        self._sub_language = subLanguages
        self.subLanguages = parse(self._sub_language, Language)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'language:{self.name}'


class AltLabel:
    def __init__(self, mode=1, text="", langIdent=""):
        self.mode = AltLabelMode(mode)
        self.text = text
        self.langIdent = langIdent

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.mode} {self.text} {self.langIdent}'


class ValueRange:
    def __init__(self, **kwargs):
        self.range_from = kwargs['from']
        self.range_to = kwargs['to']

    def __repr__(self):
        return f'range: {self.range_from} - {self.range_to}'


class ValueRef:
    def __init__(self, variableIdent="", valueIdent=""):
        self.variable_ident = variableIdent
        self.value_ident = valueIdent

    def __str__(self):
        a = f'variable_ident:{self.variable_ident}, ' \
            f'value_ident:{self.value_ident} '
        return a

    def __repr__(self):
        a = f'variable_ident:{self.variable_ident}, ' \
            f'value_ident:{self.value_ident} '
        return a


class Value:
    def __init__(self, ident="", code="", label=None, score=0, ref=None):
        if ref is None:
            ref = {}
        if label is None:
            label = []

        self.ident = ident
        self.code = code
        self._label = Label(**label)
        self.score = score
        self._ref = ref
        self.ref = ValueRef(**ref)

    @property
    def label(self):
        return f'{self.ident} - {self._label.text}'

    def __str__(self):
        return f'{self.ident} - {self._label.text}'

    def __repr__(self):
        return self.label

    def to_dict(self):
        _dict = {
            'value_code': self.code,
            'value_ident': self.ident,
            'value_label': self.label,
            'value_score': self.score}
        return _dict


class VariableValues:
    def __init__(self, range=None, values=None):
        self._range = range
        self._values = values
        self.values = parse(self._values, Value)

        if self._range is not None:
            self.range = ValueRange(**self._range)


class OtherSpecifyVariable(Variable):
    def __init__(self,
                 ordinal=0,
                 label=None,
                 name="",
                 ident="",
                 type="",
                 values=None,
                 use="",
                 maxResponses=0,
                 loopedVariables=None,
                 otherSpecifyVariables=None,
                 parentValueIdent=""):
        super().__init__(ordinal=ordinal,
                         label=label,
                         name=name,
                         ident=ident,
                         type=type,
                         values=values,
                         use=use,
                         maxResponses=maxResponses,
                         loopedVariables=loopedVariables,
                         otherSpecifyVariables=otherSpecifyVariables)
        self.parentValueIdent = parentValueIdent


class LoopedVariable(Variable):
    def __init__(self,
                 ordinal=0,
                 label=None,
                 name="",
                 ident="",
                 type="",
                 values=None,
                 use="",
                 maxResponses=0,
                 loopedVariables=None,
                 otherSpecifyVariables=None,
                 loop_ref=None):
        super().__init__(ordinal=ordinal,
                         label=label,
                         name=name,
                         ident=ident,
                         type=type,
                         values=values,
                         use=use,
                         maxResponses=maxResponses,
                         loopedVariables=loopedVariables,
                         otherSpecifyVariables=otherSpecifyVariables)

        self.loop_ref = loop_ref

    @property
    def parent_variable_ident(self):
        return self.loop_ref.variable_ident

    @property
    def parent_value_ident(self):
        return self.loop_ref.value_ident

    def to_dict(self):
        _dict = {
            'var_name': self.name,
            'variable_name': self.name,
            'variable_ident': self.ident,
            'variable_label': self.label_text,
            'variable_type': self.type.name,
            'variable_interview_label': self.label_interview,
            'variable_analysis_label': self.label_analysis,
            'parent_variable_label': self.parent_variable_ident,
            'parent_value_label': self.parent_value_ident,

        }
        if self.range:
            _dict['variable_range_from'] = self.range_from
            _dict['variable_range_to'] = self.range_to
        return _dict

    def __str__(self):
        return f'{self.name} - {self.parent_value_ident}'

    def __repr__(self):
        return f'{self.name} - {self.parent_value_ident}'


class Hierarchy:
    def __init__(self, ident: str = "", parent=None, metadata=None):
        if metadata is None:
            metadata = {}
        if parent is None:
            parent = {}
        self.ident: str = ident
        self.parent: ParentDetails = parent
        self.metadata: MetaData = metadata


class ParentDetails:
    def __init__(self, level, linkVar, ordered):
        self.level = level
        self.link_var = linkVar
        self.ordered = ordered


class MetaData:
    def __init__(self, name="", title="", interviewCount=0, languages=None,
                 notAsked="", noAnswer="", variables=None, sections=None):
        self._languages = languages
        self.name = name
        self.title = title
        self.interviewCount = interviewCount
        self.not_asked = notAsked
        self.no_answer = noAnswer
        self._variables = variables
        self._sections = sections
        self.sections = []
        self.variables = []
        self.languages = []

        if self._languages is not None:
            for _l in self._languages:
                language = Language(**_l)
                self.languages.append(language)

        if self._sections is not None:
            for _s in self._sections:
                section = Section(**_s)
                self.sections.append(section)

        if self._variables is not None:
            for _v in self._variables:
                variable = Section(**_v)
                self.variables.append(variable)


class InterviewsQuery:
    def __init__(self,
                 surveyId="",
                 start=0,
                 maxLength=0,
                 completeOnly=True,
                 variables=None,
                 interviewIdents=None,
                 date=""):
        self.survey_id = surveyId
        self.start = start
        self.max_length = maxLength
        self.complete_only = completeOnly
        self.variables = variables
        self.interview_idents = interviewIdents
        self.date = date


class LoopRef:
    def __init__(self, variableIdent, valueIdent):
        self.variable_ident = variableIdent
        self.value_ident = valueIdent


class DataItem:
    def __init__(self, ident="", values=None, loopRef=None):
        self.ident = ident
        self._values = values
        self._loop_refs = loopRef


class Level:
    def __init__(self, ident=""):
        self.ident = ""


class HierarchicalInterview:
    def __init__(self, level=None, ident="", date="", complete=True,
                 dataItems=None, hierarchicalInterviews=None):
        if hierarchicalInterviews is None:
            hierarchicalInterviews = []
        if dataItems is None:
            dataItems = []
        self.level = level
        self.ident = ident
        self.date = date
        self.complete = complete
        self._data_items = dataItems
        self._hierarchical_interviews = hierarchicalInterviews


class Interview:
    def __init__(self, ident="", date="", complete=True, dataItems=None,
                 hierarchicalInterviews=None):
        self.ident = ident
        self.date = date
        self.complete = complete
        self._data_items = dataItems
        self._hierarchical_interviews = hierarchicalInterviews


class SurveyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_surveys():
    r = requests.get(f'{SERVER}/Surveys')
    a = json.loads(r.text)
    print("Status:", r.status_code)
    return a


def get_survey_detail(s_id):
    print(f'Survey:, {s_id}')
    url = f'{SERVER}/Surveys/{s_id}/Metadata'
    print(url)
    r = requests.get(url)
    a = json.loads(r.text)

    return a


def get_survey_detail_json(s_id):
    print(f'Survey:, {s_id}')
    url = f'{SERVER}/Surveys/{s_id}/Metadata'
    print(url)
    r = requests.get(url)

    return r


def get_survey(r):
    json_r = json.loads(r.text)
    survey_obj = Survey(**json_r)
    return survey_obj
