from typing import Callable, List, Dict, Any


def add(d, label, obj, apply_to_tsapi=False):
    if apply_to_tsapi:
        if obj is not None:
            d[label] = obj.to_tsapi()
        return d
    else:
        if obj is not None:
            d[label] = obj
        return d


def parse(list_to_parse: List[Dict[str, Any]],
          obj: Callable[..., Any]) -> List[Any]:
    list_to_return = []
    if list_to_parse is not None:
        for list_item in list_to_parse:
            list_item_obj = obj(**list_item)
            list_to_return.append(list_item_obj)
    return list_to_return


# def parse(list_to_parse: list, obj: object) -> list:
#     list_to_return = []
#     if list_to_parse is not None:
#         for list_item in list_to_parse:
#             list_item_obj = obj(**list_item)
#             list_to_return.append(list_item_obj)
#     return list_to_return


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


class SurveyMetadata:
    """
    Object representing a survey and all of its metadata (information about
    questionnaire variables)

    """

    def __init__(self,
                 hierarchies=None,
                 name="",
                 title="",
                 interviewCount=0,
                 languages=None,
                 variables=None,
                 sections=None):
        self.hierarchies = parse(hierarchies, Hierarchy)
        self.name = name
        self.title = title
        self.interview_count = interviewCount
        self.variables = parse(variables, Variable)
        self.sections = parse(sections, Section)
        self.languages = parse(languages, Language)

    def __str__(self):
        return f'Name: {self.name}, Title {self.title}'

    def __repr__(self):
        return f'Survey({self.name})'

    def get_variables_list(self):
        variable_objects = ['variables',
                            'looped_variable',
                            'other_specify_variable',
                            ]
        objects_with_variables = ['survey', 'sections', 'hierarchies', ]
        objects_with_variables += variable_objects

        _dict = {}
        _dict = vars(self)

        return _dict

    def to_tsapi(self):
        _dict = {
            'hierarchies': [h.to_tsapi() for h in self.hierarchies],
            'name': self.name,
            'title': self.title,
            'interviewCount': self.interview_count,
            'languages': [lang.to_tsapi() for lang in self.languages],
            'variables': [v.to_tsapi() for v in self.variables],
            'sections': [sect.to_tsapi() for sect in self.sections]
        }
        return _dict


class Section:
    """
    Object representing a section within a survey. Sections are used to
    partition variables together into logical groups (e.g. Screener, System,
    Demographics, Main Survey etc…)
    """

    def __init__(self, label="", variables=None, sections=None):
        self.label = Label(**label)
        self.sections = parse(sections, Section)
        self.variables = parse(variables, Variable)

    def __str__(self):
        return f'{self.label}'

    def __repr__(self):
        return f'{self.label}'

    def to_tsapi(self):
        _dict = {
            'label': self.label.to_tsapi(),
            'variables': [v.to_tsapi() for v in self.variables],
            'sections': [s.to_tsapi() for s in self.sections],

        }
        return _dict


class Label:
    """
    Object representing a text label within a survey
    """

    def __init__(self, text, altLabels=None):

        self.text = text
        self.alt_labels = parse(altLabels, AltLabel)

    def __str__(self):
        return self.text

    @property
    def label_analysis(self) -> str:
        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == 'analysis':
                    alt_text = alts.text
                    return alt_text
        return alt_text

    @property
    def label_interview(self) -> str:
        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == 'interview':
                    return alts.text
        return alt_text

    def to_tsapi(self):
        _dict = {}
        _dict = add(_dict, 'text', self.text)
        if len(self.alt_labels) > 0:
            _dict['altLabels'] = [al.to_tsapi() for al in self.alt_labels]
        return _dict


class Variable:
    """	Object representing a variable or question within a survey"""

    def __init__(self,
                 variableId="",
                 ordinal=0,
                 type="",
                 name="",
                 label=None,
                 use="",
                 values=None,
                 maxResponses=0,
                 loopedVariables=None,
                 otherSpecifyVariables=None):
        self.variableId: str = variableId
        self.ordinal: int = ordinal
        self.type: str = type
        self.name: str = name
        self.label: Label = Label(**label)
        self.use: str = use
        self.maxResponses: int = maxResponses
        self.otherSpecifyVariables = parse(otherSpecifyVariables,
                                           OtherSpecifyVariable)
        if values is None:
            values = {}
        self.variable_values = VariableValues(**values)

        self.looped_variables = parse(loopedVariables, Variable)

    def to_tsapi(self):

        _dict = {}
        _dict = add(_dict, 'variableId', self.variableId)
        _dict = add(_dict, 'ordinal', self.ordinal)
        _dict = add(_dict, 'type', self.type)
        _dict = add(_dict, 'name', self.name)
        _dict = add(_dict, 'label', self.label, True)
        _dict = add(_dict, 'use', self.use)
        _dict = add(_dict, 'values', self.variable_values, True)
        _dict = add(_dict, 'maxResponses', self.maxResponses)
        if len(self.looped_variables) > 0:
            _dict['loopedVariables'] = [lv.to_tsapi()
                                        for lv in self.looped_variables],
        if len(self.otherSpecifyVariables) > 0:
            _dict['otherSpecifyVariables'] = [o.to_tsapi() for o in
                                              self.otherSpecifyVariables],

        return _dict

    @property
    def looped_variable_values(self):
        looped_variable_value_list = []
        if len(self.values) == 0 | len(self.looped_variables) == 0:
            return looped_variable_value_list

        for value in self.values:
            for l_v in self.looped_variables:
                looped_variable_value_list.append(l_v)
        return looped_variable_value_list

    def __str__(self):
        return f'{self.variableId}'

    def __repr__(self):
        return f'{self.variableId}'

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
        if self.variable_values.range:
            _r = self.variable_values.range.range_from
        return _r

    @property
    def range_to(self):
        _r = ""
        if self.variable_values.range:
            _r = self.variable_values.range.range_to
        return _r

    def range(self):
        return self.variable_values.range

    def to_dict(self):
        _dict = {
            'var_name': self.name,
            'variable_name': self.name,
            'variable_id': self.variableId,
            'variable_label': self.label_text,
            'variable_type': self.type,
            'variable_interview_label': self.label_interview,
            'variable_analysis_label': self.label_analysis,
        }
        if self.range:
            _dict['variable_range_from'] = self.range_from
            _dict['variable_range_to'] = self.range_to
        return _dict


class Language:
    """
    Object representing a language in use within a survey
    Attributes:
    -----------
    languageId: string
    nullable: true
    The unique id that is used to refer to a language within the survey
    metadata and interview data. Although there is no restriction on
    language id, the intended values of this attribute are described in the
    official W3C XML version 1.0 specification as:- "The values of the
    attribute are language identifiers as defined by IETF (Internet Engineering
    Task Force) RFC 3066, "Tags for the Identification of Languages"
    (http://www.ietf.org/rfc/rfc3066.txt) or its successor on the Standards
    Track."

     name: string
     nullable: true
     The human-readable name used to refer to a language

    """

    def __init__(self, languageId="", name="", subLanguages=None):
        # if subLanguages is None:
        #     subLanguages = []
        self.languageId = languageId
        self.name = name
        self.sub_languages = parse(subLanguages, Language)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'language:{self.name}'

    def to_tsapi(self):
        _dict = {
            'languageId': self.languageId,
            'name': self.name
        }
        if len(self.sub_languages) > 0:
            _dict['subLanguage'] = [lang.to_tsapi()
                                    for lang in self.sub_languages]
        return _dict


class AltLabel:
    """Object representing an alternative text label
    mode: string
        nullable: true
        Signals whether a text should be used during interviewing and/or
        analysis. Two explicit modes are available: “interview” and “analysis”.
         In the absence of a mode specification, the appropriate text is
         assumed to be used in both modes. Allowable values are "interview"
         and "analysis"
    text: string
        nullable: true
        Text value to use as an alternative label
    languageId: string
        nullable: true
        Indicates that an alt label should be used when interviewing in a
        given language.
    """

    def __init__(self, mode='interview', text="", languageId=""):
        self.mode = mode
        self.text = text
        self.languageId = languageId

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.mode} {self.text} {self.languageId}'

    def to_tsapi(self):
        _dict = {
            'mode': self.mode,
            'text': self.text,
            'languageId': self.languageId
        }
        return _dict


class ValueRange:
    """Object representing a range of acceptable values for a variable
    response, e.g. 1 to 100

    # added the prefix range_ to "from" and "to" as from and to
        # are reserved python words
    """

    def __init__(self, **kwargs):
        self.range_from = kwargs['from']
        self.range_to = kwargs['to']

    def __repr__(self):
        return f'range: {self.range_from} - {self.range_to}'

    def to_tsapi(self):
        _dict = {
            'from': self.range_from,
            'to': self.range_to
        }
        return _dict


class Value:
    """
    Object representing a closed-end question response

        Attributes:
        score: float

        The optional score attribute can only be used when the variable is
        of type single. It allows score values to be assigned to the
        individual code values to be used for computing statistics such as
        Mean, Standard Deviation etc. The score_value must be a number,
        and may be positive, negative or zero, with or without a decimal
        point and decimal places.The omission of a score implies that
        records having that value code should be omitted from the base for
        any statistical computation for that variable.
    """

    def __init__(self, valueId="", code="", label=None, score=0):
        if label is None:
            label = []

        self.valueId = valueId
        self.code = code
        self.label = Label(**label)
        self.score = score

    def to_tsapi(self):
        _dict = {}
        _dict = add(_dict, 'valueId', self.valueId)
        _dict = add(_dict, 'code', self.code)
        _dict = add(_dict, 'label', self.label, True)
        _dict = add(_dict, 'score', self.score)

        return _dict

    # @property
    # def label(self):
    #     return f'{self.ident} - {self._label.text}'

    def __str__(self):
        return f'{self.valueId} - {self.label.text}'

    def __repr__(self):
        return self.label

    def to_dict(self):
        _dict = {
            'value_code': self.code,
            'value_id': self.valueId,
            'value_label': self.label.text,
            'value_score': self.score}
        return _dict


class VariableValues:
    """Object representing an allowable set of values for a variable"""

    def __init__(self, valueListId="", range=None, values=None):
        self.valueListId = valueListId
        self.range = range
        self.values = parse(values, Value)

        if self.range is not None:
            self.range = ValueRange(**self.range)

    def to_tsapi(self):
        _dict = {}
        _dict = add(_dict, 'valueListId', self.valueListId)
        if self.values is not None:
            _dict['values'] = [val.to_tsapi() for val in self.values]
        if self.range is not None:
            _dict['range'] = self.range.to_tsapi()
        return _dict


class OtherSpecifyVariable(Variable):
    """	Object representing an “other specify” variable within a closed-end
    variable
    """

    def __init__(self,
                 parentValueId="",
                 variableId="",
                 ordinal=0,
                 type="",
                 name="",
                 label=None,
                 use="",
                 values=None,
                 maxResponses=0,
                 loopedVariables=None,
                 otherSpecifyVariables=None,
                 ):
        super().__init__(
            variableId=variableId,
            ordinal=ordinal,
            label=label,
            name=name,
            type=type,
            values=values,
            use=use,
            maxResponses=maxResponses,
            loopedVariables=loopedVariables,
            otherSpecifyVariables=otherSpecifyVariables)
        self.parentValueId = parentValueId

    def to_tsapi(self):
        _dict = {}
        _dict = add(_dict, 'parentValueId', self.parentValueId)
        _dict = add(_dict, 'variableId', self.variableId)
        _dict = add(_dict, 'ordinal', self.ordinal)
        _dict = add(_dict, 'type', self.type)
        _dict = add(_dict, 'name', self.name)
        _dict = add(_dict, 'label', self.label, True)
        _dict = add(_dict, 'use', self.use)
        _dict = add(_dict, 'values', self.variable_values, True)
        _dict = add(_dict, 'maxResponses', self.maxResponses)
        _dict['loopedVariables'] = [lv.to_tsapi() for lv in
                                    self.looped_variables]
        _dict['otherSpecifyVariables'] = [o.to_tsapi() for o in
                                          self.otherSpecifyVariables]
        return _dict


#
# class LoopedVariable(Variable):
#
#     def __init__(self,
#                  variableId="",
#                  ordinal=0,
#                  label=None,
#                  name="",
#                  type="",
#                  values=None,
#                  use="",
#                  maxResponses=0,
#                  loopedVariables=None,
#                  otherSpecifyVariables=None,
#                  loop_ref=None):
#         super().__init__(variableId=variableId,
#                          ordinal=ordinal,
#                          label=label,
#                          name=name,
#                          type=type,
#                          values=values,
#                          use=use,
#                          maxResponses=maxResponses,
#                          loopedVariables=loopedVariables,
#                          otherSpecifyVariables=otherSpecifyVariables)
#
#         self.loop_ref = loop_ref
#
#     def to_tsapi(self):
#         _dict = {}
#         _dict = add(_dict, 'ordinal', self.ordinal)
#         _dict = add(_dict, 'label', self.label, True)
#         _dict = add(_dict, 'name', self.name)
#         _dict = add(_dict, 'ident', self.ident)
#         _dict = add(_dict, 'type', self.type)
#         _dict = add(_dict, 'values', self.variable_values, True)
#         _dict = add(_dict, 'use', self.use)
#         _dict = add(_dict, 'maxResponses', self.maxResponses)
#         _dict['loopedVariables'] = [lv.to_tsapi() for lv in
#                                     self.looped_variables]
#         _dict['otherSpecifyVariables'] = [o.to_tsapi() for o in
#                                           self.otherSpecifyVariables]
#         _dict = add(_dict, 'loopRef', self.loop_ref, True)
#
#         return _dict
#
#     @property
#     def parent_variable_ident(self):
#         if self.loop_ref is not None:
#             return self.loop_ref.variable_ident
#         else:
#             return ""
#
#     @property
#     def parent_value_ident(self):
#         if self.loop_ref is not None:
#             return self.loop_ref.value_ident
#         else:
#             return ""
#
#     def to_dict(self):
#         _dict = {
#             'var_name': self.name,
#             'variable_name': self.name,
#             'variable_ident': self.ident,
#             'variable_label': self.label_text,
#             'variable_type': self.type,
#             'variable_interview_label': self.label_interview,
#             'variable_analysis_label': self.label_analysis,
#             'parent_variable_label': self.parent_variable_ident,
#             'parent_value_label': self.parent_value_ident,
#
#         }
#         if self.range:
#             _dict['variable_range_from'] = self.range_from
#             _dict['variable_range_to'] = self.range_to
#         return _dict
#
#     def __str__(self):
#         return f'{self.name} - {self.parent_value_ident}'
#
#     def __repr__(self):
#         return f'{self.name}'


class Hierarchy:
    """Represents a hierarchical sub-questionnaire within a main survey"""

    def __init__(self, hierarchyId: str = "", parent=None, metadata=None):
        if metadata is None:
            metadata = {}
        if parent is None:
            parent = {}
        self.hierarchyId: str = hierarchyId
        self.parent: ParentDetails = parent
        self.metadata: MetaData = metadata

    def to_tsapi(self):
        _dict = {
            'hierarchyId': self.hierarchyId,
            'metadata': self.metadata.to_tsapi(),
            'parent': self.parent
        }


class ParentDetails:
    """
    Object defining the parent and child relationship between hierarchical
    surveys
    """

    def __init__(self, level, linkVar, ordered):
        self.level = level
        self.link_var = linkVar
        self.ordered = ordered

    def to_tsapi(self):
        _dict = {
            'level': self.level,
            'linkVar': self.link_var,
            'ordered': self.ordered
        }


class MetaData:
    """The metadata (list of questions and variables) for a hierarchy item"""

    def __init__(self, name="", title="", interviewCount=0, languages=None,
                 notAsked="", noAnswer="", variables=None, sections=None):
        self.name = name
        self.title = title
        self.interview_count = interviewCount
        self.not_asked = notAsked
        self.no_answer = noAnswer
        self.sections = parse(sections, Section)
        self.variables = parse(variables, Variable)
        self.languages = parse(languages, Language)

    def to_tsapi(self):
        _dict = {
            'name': self.name,
            'title': self.name,
            'interviewCount': self.interview_count,
            'notAsked': self.not_asked,
            'noAnswer': self.no_answer,
            'variables': [var.to_tsapi() for var in self.variables],
            'sections': [sect.to_tsapi() for sect in self.sections],
            'languages': [lang.to_tsapi() for lang in self.languages],
        }
        return _dict


# class InterviewsQuery:
#     def __init__(self,
#                  surveyId="",
#                  start=0,
#                  maxLength=0,
#                  completeOnly=True,
#                  variables=None,
#                  interviewIdents=None,
#                  date=""):
#         self.survey_id = surveyId
#         self.start = start
#         self.max_length = maxLength
#         self.complete_only = completeOnly
#         self.variables = variables
#         self.interview_idents = interviewIdents
#         self.date = date


class VariableData:
    """	Represents the response(s) given to a variable in the survey"""

    def __init__(self,
                 variableId: str = "",
                 data=None):
        self.variableId = variableId
        self.data = parse(data, VariableDataItem)

    def __str__(self):
        return f'variableId:{self.variableId}'

    def __repr__(self):
        return f'variableId:{self.variableId}'

    def to_tsapi(self):
        _dict = {
            'variableId': self.variableId,
            'data': [d.to_tsapi() for d in self.data],
        }
        return _dict


class VariableDataItem:
    """Object representing a data value or response for a variable in an
    interview"""

    def __init__(self,
                 value: str = "",
                 state: str = "",
                 loopedVariableData=None):
        self.value = value
        self.state = state
        self.loopedVariableData = parse(loopedVariableData, VariableData)

    def to_tsapi(self):
        _dict = {
            'value': self.value,
            #'state': self.state,

            #'loopedVariableData': [d.to_tsapi() for d
                                   #in self.loopedVariableData],
        }
        if self.state != "":
            _dict['state'] = self.state

        if self.loopedVariableData:
            _dict['loopedVariableData'] = [d.to_tsapi() for d
                                           in self.loopedVariableData]
        return _dict

    def __str__(self):
        return (
            f'value:{self.value} - {self.state}'
            if self.state
            else f'value:{self.value} '
        )

    def __repr__(self):
        return (
            f'value:{self.value} - {self.state}'
            if self.state
            else f'value:{self.value}'
        )


class Level:
    """ no description provided 13 Aug 2024"""

    def __init__(self, levelId=""):
        self.levelId = levelId

    def to_tsapi(self):
        _dict = {'levelId': self.levelId}
        return _dict

    def __str__(self):
        return f'levelId:{self.levelId}'

    def __repr__(self):
        return f'levelId:{self.levelId}'


class HierarchicalInterview:
    def __init__(self, level=None, interviewId="", date="", complete=True,
                 responses=None, hierarchicalInterviews=None):
        self.level = Level(**level)
        self.interviewId = interviewId
        self.date = date
        self.complete = complete
        self.responses = parse(responses, VariableData)
        self.hierarchical_interviews = parse(hierarchicalInterviews,
                                             HierarchicalInterview)

    def to_tsapi(self):
        _dict = {'level': self.level.to_tsapi(),
                 'interviewId': self.interviewId,
                 'date': self.date,
                 'complete': self.complete,
                 'responses': [di.to_tsapi() for di in self.responses],
                 'hierarchicalInterviews': [hi.to_tsapi() for hi in
                                            self.hierarchical_interviews]}
        return _dict

    def __str__(self):
        return f'interviewId:{self.interviewId} - date: {self.date}'

    def __repr__(self):
        return f'interviewId:{self.interviewId} - date: {self.date}'


class Interview:
    def __init__(self, interviewId="", date="", complete=True, responses=None,
                 hierarchicalInterviews=None):
        self.interviewId = interviewId
        self.date = date
        self.complete = complete
        self.responses = parse(responses, VariableData)
        self.hierarchical_interviews = parse(hierarchicalInterviews,
                                             HierarchicalInterview)

    def __str__(self):
        return f'interviewId:{self.interviewId} - date: {self.date}'

    def __repr__(self):
        return f'interviewId:{self.interviewId} - date: {self.date}'

    def to_tsapi(self):
        _dict = {'interviewId': self.interviewId,
                 'date': self.date,
                 'complete': self.complete,
                 'responses': [di.to_tsapi() for di in self.responses]}
        if self.hierarchical_interviews:
            _dict['hierarchicalInterviews'] = [hi.to_tsapi() for hi in
                                               self.hierarchical_interviews]

        return _dict
