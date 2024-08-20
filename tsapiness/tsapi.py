from .utils import add, parse
from datetime import date


class SurveyMetadata:
    """
    Object representing a survey and all of its metadata (information about
    questionnaire variables)

    Attributes:
        hierarchies (list): List of hierarchies in the survey.
        name (str): Name of the survey.
        title (str): Title of the survey.
        interview_count (int): Number of interviews.
        languages (list): List of languages used in the survey.
        variables (list): List of variables in the survey.
        sections (list): List of sections in the survey.
    """

    def __init__(self,
                 hierarchies=None,
                 name="",
                 title="",
                 interviewCount=0,
                 languages=None,
                 variables=None,
                 sections=None):
        """
        Initializes a SurveyMetadata object.

        Args:
            hierarchies (list, optional): List of hierarchies in the survey.
            name (str, optional): Name of the survey.
            title (str, optional): Title of the survey.
            interviewCount (int, optional): Number of interviews.
            languages (list, optional): List of languages used in the survey.
            variables (list, optional): List of variables in the survey.
            sections (list, optional): List of sections in the survey.
        """

        self.hierarchies = parse(hierarchies, Hierarchy)
        self.name = name
        self.title = title
        self.interview_count = interviewCount
        self.variables = parse(variables, Variable)
        self.sections = parse(sections, Section)
        self.languages = parse(languages, Language)

    def __str__(self):
        """
        Returns a string representation of the SurveyMetadata object.

        Returns:
            str: String representation of the survey metadata.
        """
        return f'Name: {self.name}, Title {self.title}'

    def __repr__(self):
        """
        Returns a detailed string representation of the SurveyMetadata object.

        Returns:
            str: Detailed string representation of the survey metadata.
        """
        return f'Survey({self.name})'

    def get_variables_list(self):
        """
        Retrieves a dictionary of variables and their associated objects.

        Returns:
            dict: Dictionary of variables and their associated objects.
        """

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
        """
        Converts the SurveyMetadata object to a dictionary in the TSAPI format.

        return:
            dict: Dictionary in the TSAPI format representing the survey
            metadata.

        """
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
        """
        Initializes a Section object.

        Args:
            label (dict, optional): A dictionary representing the label of the
            section.
            variables (list, optional): A list of Variable objects within the
            section.
            sections (list, optional): A list of nested Section objects within
            the section.
        """
        self.label = Label(**label or {})
        self.sections = parse(sections, Section)
        self.variables = parse(variables, Variable)

    def __str__(self):
        """
        Returns a string representation of the Section object.

        Returns:
            str: String representation of the section label.
        """
        return f'{self.label}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Section object.

        Returns:
            str: Detailed string representation of the section label.
        """
        return f'{self.label}'

    def to_tsapi(self):
        """
        Converts the Section object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the section.
        """
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

    def __init__(self, text="", altLabels=None):
        """
        Initializes a Label object.

        Args:
            text (str, optional): The main text of the label.
            altLabels (list, optional): A list of AltLabel objects representing
            alternative labels.
        """
        self.text = text
        self.alt_labels = parse(altLabels, AltLabel)

    def __str__(self):
        """
        Returns a string representation of the Label object.

        Returns:
            str: The main text of the label.
        """
        return self.text

    @property
    def label_analysis(self) -> str:
        """
        Retrieves the analysis mode alternative label text.

        Returns:
            str: The text of the analysis mode alternative label, if available.
        """
        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == 'analysis':
                    alt_text = alts.text
                    return alt_text
        return alt_text

    @property
    def label_interview(self) -> str:
        """
        Retrieves the interview mode alternative label text.

        Returns:
            str: The text of the interview mode alternative label, if
            available.
        """

        alt_text = ""
        if self.alt_labels:
            for alts in self.alt_labels:
                if alts.mode == 'interview':
                    return alts.text
        return alt_text

    def to_tsapi(self):
        """
        Initializes a Section object.

        Args:
            label (dict, optional): A dictionary representing the label of the
            section.
            variables (list, optional): A list of Variable objects within the
            section.
            sections (list, optional): A list of nested Section objects within
            the section.
        """
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
        """
        Initializes a Variable object.

        Args:
            variableId (str, optional): The unique identifier for the variable.
            ordinal (int, optional): The ordinal position of the variable.
            type (str, optional): The type of the variable.
            name (str, optional): The name of the variable.
            label (dict, optional): A dictionary representing the label of the
            variable.
            use (str, optional): The intended use of the variable.
            values (dict, optional): A dictionary representing the values of
            the variable.
            maxResponses (int, optional): The maximum number of responses
            allowed.
            loopedVariables (list, optional): A list of looped Variable
            objects.
            otherSpecifyVariables (list, optional): A list of
            OtherSpecifyVariable objects.
        """
        self.variableId: str = variableId
        self.ordinal: int = ordinal
        self.type: str = type
        self.name: str = name
        self.label: Label = Label(**label or {})
        self.use: str = use
        self.maxResponses: int = maxResponses
        self.otherSpecifyVariables = parse(otherSpecifyVariables,
                                           OtherSpecifyVariable)
        if values is None:
            values = {}
        self.variable_values = VariableValues(**values)

        self.looped_variables = parse(loopedVariables, Variable)

    def to_tsapi(self):
        """
        Converts the Variable object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the variable.
        """
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
        """
        Retrieves a list of looped variable values.

        Returns:
            list: List of looped variable values.
        """

        looped_variable_value_list = []
        if len(self.values) == 0 | len(self.looped_variables) == 0:
            return looped_variable_value_list

        for value in self.values:
            for l_v in self.looped_variables:
                looped_variable_value_list.append(l_v)
        return looped_variable_value_list

    def __str__(self):
        """
        Returns a string representation of the Variable object.

        Returns:
            str: String representation of the variable ID.
        """
        return f'{self.variableId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Variable object.

        Returns:
            str: Detailed string representation of the variable ID.
        """
        return f'{self.variableId}'

    @property
    def alt_labels(self):
        """
        Retrieves the alternative labels of the variable.

        Returns:
            list: List of alternative labels.
        """
        return self.label.alt_labels

    @property
    def label_text(self):
        """
        Retrieves the main text of the variable's label.

        Returns:
            str: The main text of the label.
        """
        return self.label.text

    @property
    def values(self):
        """
        Retrieves the values of the variable.

        Returns:
            list: List of values.
        """
        return self.variable_values.values

    @property
    def label_interview(self):
        """
        Retrieves the interview mode alternative label text.

        Returns:
            str: The text of the interview mode alternative label, if
            available.
        """
        return self.label.label_interview

    @property
    def label_analysis(self):
        """
        Retrieves the analysis mode alternative label text.

        Returns:
            str: The text of the analysis mode alternative label, if available.
        """
        return self.label.label_analysis

    @property
    def range_from(self):
        """
        Retrieves the starting value of the variable's range.

        Returns:
            str: The starting value of the range.
        """
        _r = ""
        if self.variable_values.range:
            _r = self.variable_values.range.range_from
        return _r

    @property
    def range_to(self):
        """
        Retrieves the ending value of the variable's range.

        Returns:
            str: The ending value of the range.
        """
        _r = ""
        if self.variable_values.range:
            _r = self.variable_values.range.range_to
        return _r

    def range(self):
        """
        Retrieves the range of the variable.

        Returns:
            ValueRange: The range of the variable.
        """
        return self.variable_values.range

    def to_dict(self):
        """
        Converts the Variable object to a dictionary.

        Returns:
            dict: Dictionary representing the variable.
        """
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
    Object representing a language in use within a survey.

    Attributes:
    -----------
    languageId: string
        The unique id that is used to refer to a language within the survey
        metadata and interview data. Although there is no restriction on
        language id, the intended values of this attribute are described in the
        official W3C XML version 1.0 specification as:- "The values of the
        attribute are language identifiers as defined by IETF (Internet
        Engineering Task Force) RFC 3066, "Tags for the Identification of
        Languages" (http://www.ietf.org/rfc/rfc3066.txt) or its successor on
        the Standards Track."
    name: string
        The human-readable name used to refer to a language.
    """

    def __init__(self, languageId="", name="", subLanguages=None):
        """
        Initializes a Language object.

        Args:
            languageId (str, optional): The unique id of the language.
            name (str, optional): The human-readable name of the language.
            subLanguages (list, optional): A list of sub-language objects.
        """
        self.languageId = languageId
        self.name = name
        self.sub_languages = parse(subLanguages, Language)

    def __str__(self):
        """
        Returns a string representation of the Language object.

        Returns:
            str: The name of the language.
        """
        return f'{self.name}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Language object.

        Returns:
            str: Detailed string representation of the language.
        """
        return f'language:{self.name}'

    def to_tsapi(self):
        """
        Converts the Language object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the language.
        """
        _dict = {
            'languageId': self.languageId,
            'name': self.name
        }
        if len(self.sub_languages) > 0:
            _dict['subLanguage'] = [lang.to_tsapi()
                                    for lang in self.sub_languages]
        return _dict


class AltLabel:
    """
    Object representing an alternative text label.

    Attributes:
        mode (str): Signals whether a text should be used during interviewing
        and/or analysis.
                    Two explicit modes are available: "interview" and
                    "analysis".
                    In the absence of a mode specification, the appropriate
                    text is assumed to be used in both modes.
        text (str): Text value to use as an alternative label.
        languageId (str): Indicates that an alt label should be used when
        interviewing in a given language.
    """

    def __init__(self, mode='interview', text="", languageId=""):
        """
         Initializes an AltLabel object.

         Args:
             mode (str, optional): The mode of the label. Defaults to
             'interview'.
             text (str, optional): The text of the label. Defaults to an empty
             string.
             languageId (str, optional): The language ID for the label.
             Defaults to an empty string.
         """
        self.mode = mode
        self.text = text
        self.languageId = languageId

    def __str__(self):
        """
        Returns a string representation of the AltLabel object.

        Returns:
            str: The text of the label.
        """
        return self.text

    def __repr__(self):
        """
        Returns a detailed string representation of the AltLabel object.

        Returns:
            str: Detailed string representation of the label.
        """
        return f'{self.mode} {self.text} {self.languageId}'

    def to_tsapi(self):
        """
        Converts the AltLabel object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the label.
        """
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
        """
        Initializes a ValueRange object.

        Args:
            **kwargs: Arbitrary keyword arguments. Expected keys are 'from'
            and 'to'.
        """
        self.range_from = kwargs['from']
        self.range_to = kwargs['to']

    def __str__(self):
        """
        Returns a string representation of the ValueRange object.

        Returns:
            str: String representation of the range.
        """
        return f'{self.range_from} - {self.range_to}'

    def __repr__(self):
        """
        Returns a detailed string representation of the ValueRange object.

        Returns:
            str: Detailed string representation of the range.
        """
        return f'range: {self.range_from} - {self.range_to}'

    def to_tsapi(self):
        """
        Converts the ValueRange object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the range.
        """
        _dict = {
            'from': self.range_from,
            'to': self.range_to
        }
        return _dict


class Value:
    """
    Object representing a closed-end question response.

    Attributes:
        valueId (str): The unique identifier for the value.
        code (str): The code associated with the value.
        label (Label): The label object associated with the value.
        score (float): The score associated with the value. The score can only
        be used when the variable is of type single. It allows score values to
        be assigned to the individual code values to be used for computing
        statistics such as Mean, Standard Deviation etc. The score_value must
        be a number, and may be positive, negative or zero, with or without a
        decimal point and decimal places. The omission of a score implies that
         records having that value code should be omitted from the base for any
         statistical computation for that variable.
    """

    def __init__(self, valueId="", code="", label=None, score=0):
        """
        Initializes a Value object.

        Args:
            valueId (str, optional): The unique identifier for the value.
            Defaults to an empty string.
            code (str, optional): The code associated with the value.
            Defaults to an empty string.
            label (dict, optional): A dictionary representing the label of
            the value. Defaults to None.
            score (float, optional): The score associated with the value.
            Defaults to 0.
        """
        if label is None:
            label = []

        self.valueId = valueId
        self.code = code
        self.label = Label(**label)
        self.score = score

    def to_tsapi(self):
        """
        Converts the Value object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the value.
        """
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
        """
        Returns a string representation of the Value object.

        Returns:
            str: String representation of the value ID and label text.
        """
        return f'{self.valueId} - {self.label.text}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Value object.

        Returns:
            str: Detailed string representation of the label.
        """
        return self.label

    def to_dict(self):
        """
        Converts the Value object to a dictionary.

        Returns:
            dict: Dictionary representing the value.
        """
        _dict = {
            'value_code': self.code,
            'value_id': self.valueId,
            'value_label': self.label.text,
            'value_score': self.score}
        return _dict


class VariableValues:
    """
    Object representing an allowable set of values for a variable.

    Attributes:
        valueListId (str): The ID of the value list.
        range (ValueRange): The range of acceptable values.
        values (list): A list of Value objects representing the allowable
        values.
    """

    def __init__(self, valueListId="", range=None, values=None):
        """
        Initializes a VariableValues object.

        Args:
            valueListId (str, optional): The ID of the value list. Defaults
            to an empty string.
            range (ValueRange, optional): The range of acceptable values.
            Defaults to None.
            values (list, optional): A list of Value objects representing the
            allowable values. Defaults to None.
        """
        self.valueListId = valueListId
        self.range = range
        self.values = parse(values, Value)

        if self.range is not None:
            self.range = ValueRange(**self.range)

    def __str__(self):
        """
        Returns a string representation of the VariableValues object.

        Returns:
            str: String representation of the value list ID.
        """
        return f'{self.valueListId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the VariableValues object.

        Returns:
            str: Detailed string representation of the value list ID.
        """
        return f'{self.valueListId}'

    def to_tsapi(self):
        """
        Converts the VariableValues object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the variable
            values.
        """
        _dict = {}
        _dict = add(_dict, 'valueListId', self.valueListId)
        if self.values is not None:
            _dict['values'] = [val.to_tsapi() for val in self.values]
        if self.range is not None:
            _dict['range'] = self.range.to_tsapi()
        return _dict


class OtherSpecifyVariable(Variable):
    """
    Object representing an "other specify" variable within a closed-end
    variable.

    Attributes:
        parentValueId (str): The ID of the parent value.
        variableId (str): The unique identifier for the variable.
        ordinal (int): The ordinal position of the variable.
        type (str): The type of the variable.
        name (str): The name of the variable.
        label (Label): The label object associated with the variable.
        use (str): The intended use of the variable.
        values (VariableValues): The values associated with the variable.
        maxResponses (int): The maximum number of responses allowed.
        loopedVariables (list): A list of looped Variable objects.
        otherSpecifyVariables (list): A list of OtherSpecifyVariable objects.
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
        """
        Initializes an OtherSpecifyVariable object.

        Args:
            parentValueId (str, optional): The ID of the parent value. Defaults
            to an empty string.
            variableId (str, optional): The unique identifier for the variable.
            Defaults to an empty string.
            ordinal (int, optional): The ordinal position of the variable.
            Defaults to 0.
            type (str, optional): The type of the variable.
            Defaults to an empty string.
            name (str, optional): The name of the variable.
            Defaults to an empty string.
            label (dict, optional): A dictionary representing the label of the
            variable. Defaults to None.
            use (str, optional): The intended use of the variable. Defaults to
            an empty string.
            values (dict, optional): A dictionary representing the values of
            the variable. Defaults to None.
            maxResponses (int, optional): The maximum number of responses
            allowed. Defaults to 0.
            loopedVariables (list, optional): A list of looped Variable
            objects. Defaults to None.
            otherSpecifyVariables (list, optional): A list of
            OtherSpecifyVariable objects. Defaults to None.
        """
        super().__init__(
            variableId=variableId,
            ordinal=ordinal,
            label=label or {},
            name=name,
            type=type,
            values=values,
            use=use,
            maxResponses=maxResponses,
            loopedVariables=loopedVariables,
            otherSpecifyVariables=otherSpecifyVariables)
        self.parentValueId = parentValueId

    def __str__(self):
        """
        Returns a string representation of the OtherSpecifyVariable object.

        Returns:
            str: String representation of the variableID.
        """
        return f'{self.variableId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the OtherSpecifyVariable
        object.

        Returns:
            str: Detailed string representation of the variableId
        """
        return f'{self.variableId}'

    def to_tsapi(self):
        """
        Converts the OtherSpecifyVariable object to a dictionary in the TSAPI
        format.

        Returns:
            dict: Dictionary in the TSAPI format representing the other
            specify variable.
        """
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


class Hierarchy:
    """
    Object representing a hierarchical interview.

    Attributes:
        hierarchyId (str): The unique identifier for the hierarchy.
        parent (ParentDetails): The parent details of the hierarchy.
        metadata (MetaData): The metadata associated with the hierarchy.
    """

    def __init__(self, hierarchyId: str = "", parent=None, metadata=None):
        """
        Initializes a Hierarchy object.

        Args:
            hierarchyId (str, optional): The unique identifier for the
            hierarchy. Defaults to an empty string.
            parent (ParentDetails, optional): The parent details of the
            hierarchy. Defaults to None.
            metadata (MetaData, optional): The metadata associated with the
            hierarchy. Defaults to None.
        """
        if metadata is None:
            metadata = {}
        if parent is None:
            parent = {}
        self.hierarchyId: str = hierarchyId
        self.parent: ParentDetails = parent
        self.metadata: MetaData = metadata

    def __str__(self):
        """
        Returns a string representation of the Hierarchy object.

        Returns:
            str: String representation of the hierarchy ID.
        """
        return f'hierarchyId:{self.hierarchyId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the HierarchicalInterview
        object.

        Returns:
            str: Detailed string representation of the interview ID and date.
        """
        return f'hierarchyId:{self.hierarchyId}'

    def to_tsapi(self):
        """
        Converts the Hierarchy object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the hierarchy.
        """
        _dict = {
            'hierarchyId': self.hierarchyId,
            'metadata': self.metadata.to_tsapi(),
            'parent': self.parent
        }
        return _dict


class ParentDetails:
    """
    Object defining the parent and child relationship between hierarchical
    surveys.

    Attributes:
        level (str): The level of the hierarchy.
        link_var (str): The variable that links the parent and child.
        ordered (bool): Indicates whether the hierarchy is ordered.
    """

    def __init__(self, level, linkVar, ordered):
        """
        Initializes a ParentDetails object.

        Args:
            level (str): The level of the hierarchy.
            linkVar (str): The variable that links the parent and child.
            ordered (bool): Indicates whether the hierarchy is ordered.
        """
        self.level = level
        self.link_var = linkVar
        self.ordered = ordered

    def __str__(self):
        """
        Returns a string representation of the ParentDetails object.

        Returns:
            str: String representation of the parent details.
        """
        return f'level:{self.level}'

    def __repr__(self):
        """
        Returns a detailed string representation of the ParentDetails object.

        Returns:
            str: Detailed string representation of the parent details.
        """
        return f'level:{self.level}'

    def to_tsapi(self):
        """
        Converts the ParentDetails object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the parent
            details.
        """
        _dict = {
            'level': self.level,
            'linkVar': self.link_var,
            'ordered': self.ordered
        }
        return _dict


class MetaData:
    """
    The metadata (list of questions and variables) for a hierarchy item.

    Attributes:
        name (str): The name of the metadata.
        title (str): The title of the metadata.
        interview_count (int): The number of interviews.
        not_asked (str): The not asked status.
        no_answer (str): The no answer status.
        sections (list): A list of Section objects.
        variables (list): A list of Variable objects.
        languages (list): A list of Language objects.
    """

    def __init__(self,
                 name="",
                 title="",
                 interviewCount=0,
                 languages=None,
                 notAsked="",
                 noAnswer="",
                 variables=None,
                 sections=None):
        """
        Initializes a MetaData object.

        Args:
            name (str, optional): The name of the metadata. Defaults to an
            empty string.
            title (str, optional): The title of the metadata. Defaults to an
            empty string.
            interviewCount (int, optional): The number of interviews. Defaults
            to 0.
            languages (list, optional): A list of Language objects. Defaults
            to None.
            notAsked (str, optional): The not asked status. Defaults to an
            empty string.
            noAnswer (str, optional): The no answer status. Defaults to an
            empty string.
            variables (list, optional): A list of Variable objects. Defaults
            to None.
            sections (list, optional): A list of Section objects. Defaults
            to None.
        """
        self.name = name
        self.title = title
        self.interview_count = interviewCount
        self.not_asked = notAsked
        self.no_answer = noAnswer
        self.sections = parse(sections, Section)
        self.variables = parse(variables, Variable)
        self.languages = parse(languages, Language)

    def __str__(self):
        """
        Returns a string representation of the MetaData object.

        Returns:
            str: String representation of the metadata name.
        """
        return f'Name: {self.name}, Title {self.title}'

    def __repr__(self):
        """
        Returns a detailed string representation of the MetaData object.

        Returns:
            str: Detailed string representation of the metadata name.
        """
        return f'Name: {self.name}, Title {self.title}'

    def to_tsapi(self):
        """
        Converts the MetaData object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the metadata.
        """
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


class VariableData:
    """
    Represents the response(s) given to a variable in the survey.

    Attributes:
        variableId (str): The unique identifier for the variable.
        data (list): A list of VariableDataItem objects representing the data
        values or responses.
    """
    def __init__(self,
                 variableId: str = "",
                 data=None):
        """
        Initializes a VariableData object.

        Args:
            variableId (str, optional): The unique identifier for the variable.
            Defaults to an empty string.
            data (list, optional): A list of VariableDataItem objects.
            Defaults to None.
        """
        self.variableId = variableId
        self.data = parse(data, VariableDataItem)

    def __str__(self):
        """
        Returns a string representation of the VariableData object.

        Returns:
            str: String representation of the variable ID.
        """
        return f'variableId:{self.variableId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the VariableData object.

        Returns:
            str: Detailed string representation of the variable ID.
        """
        return f'variableId:{self.variableId}'

    def to_tsapi(self):
        """
        Converts the VariableData object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the variable
            data.
        """
        _dict = {
            'variableId': self.variableId,
            'data': [d.to_tsapi() for d in self.data],
        }
        return _dict


class VariableDataItem:
    """
    Object representing a data value or response for a variable in an
    interview.

    Attributes:
        value (str): The value of the data item.
        state (str): The state of the data item.
        loopedVariableData (list): A list of VariableData objects representing
        looped variable data.
    """

    def __init__(self,
                 value: str = "",
                 state: str = "",
                 loopedVariableData=None):
        """
        Initializes a VariableDataItem object.

        Args:
            value (str, optional): The value of the data item. Defaults to an
            empty string.
            state (str, optional): The state of the data item. Defaults to an
            empty string.
            loopedVariableData (list, optional): A list of VariableData
            objects. Defaults to None.
        """
        self.value = value
        self.state = state
        self.loopedVariableData = parse(loopedVariableData, VariableData)

    def to_tsapi(self):
        """
        Converts the VariableDataItem object to a dictionary in the TSAPI
        format.

        Returns:
            dict: Dictionary in the TSAPI format representing the variable
            data item.
        """
        _dict = {
            'value': self.value.strftime('%Y-%m-%d') if
            isinstance(self.value, date) else self.value,
        }
        if self.state != "":
            _dict['state'] = self.state

        if self.loopedVariableData:
            _dict['loopedVariableData'] = [d.to_tsapi() for d
                                           in self.loopedVariableData]
        return _dict

    def __str__(self):
        """
        Returns a string representation of the VariableDataItem object.

        Returns:
            str: String representation of the value.
        """
        return (
            f'value:{self.value} - {self.state}'
            if self.state
            else f'value:{self.value} '
        )

    def __repr__(self):
        """
        Returns a detailed string representation of the VariableDataItem
        object.

        Returns:
            str: Detailed string representation of the value.
        """

        return (
            f'value:{self.value} - {self.state}'
            if self.state
            else f'value:{self.value}'
        )


class Level:
    """
    Represents a level in a hierarchical structure.

    Attributes:
        levelId (str): The unique identifier for the level.
    """
    def __init__(self, levelId=""):
        """
        Initializes a Level object.

        Args:
            levelId (str, optional): The unique identifier for the level.
            Defaults to an empty string.
        """
        self.levelId = levelId

    def to_tsapi(self):
        """
        Converts the Level object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the level.
        """
        _dict = {'levelId': self.levelId}
        return _dict

    def __str__(self):
        """
        Returns a string representation of the Level object.

        Returns:
            str: String representation of the level ID.
        """
        return f'levelId:{self.levelId}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Level object.

        Returns:
            str: Detailed string representation of the level ID.
        """
        return f'levelId:{self.levelId}'


class HierarchicalInterview:
    """
    Represents a hierarchical interview.

    Attributes:
        level (Level): The level of the hierarchical interview.
        interviewId (str): The unique identifier for the interview.
        date (str): The date of the interview.
        complete (bool): Indicates whether the interview is complete.
        responses (list): A list of VariableData objects representing the
        responses.
        hierarchical_interviews (list): A list of nested HierarchicalInterview
        objects.
    """
    def __init__(self, level=None,
                 interviewId="",
                 date="",
                 complete=True,
                 responses=None,
                 hierarchicalInterviews=None):
        """
        Initializes a HierarchicalInterview object.

        Args:
            level (dict, optional): A dictionary representing the level.
            Defaults to None.
            interviewId (str, optional): The unique identifier for the
            interview. Defaults to an empty string.
            date (str, optional): The date of the interview. Defaults to an
            empty string.
            complete (bool, optional): Indicates whether the interview is
            complete. Defaults to True.
            responses (list, optional): A list of VariableData objects.
            Defaults to None.
            hierarchicalInterviews (list, optional): A list of nested
            HierarchicalInterview objects. Defaults to None.
        """
        self.level = Level(**level)
        self.interviewId = interviewId
        self.date = date
        self.complete = complete
        self.responses = parse(responses, VariableData)
        self.hierarchical_interviews = parse(hierarchicalInterviews,
                                             HierarchicalInterview)

    def to_tsapi(self):
        """
        Converts the HierarchicalInterview object to a dictionary in the TSAPI
        format.

        Returns:
            dict: Dictionary in the TSAPI format representing the hierarchical
            interview.
        """
        _dict = {'level': self.level.to_tsapi(),
                 'interviewId': self.interviewId,
                 'date': self.date,
                 'complete': self.complete,
                 'responses': [di.to_tsapi() for di in self.responses],
                 'hierarchicalInterviews': [hi.to_tsapi() for hi in
                                            self.hierarchical_interviews]}
        return _dict

    def __str__(self):
        """
        Returns a string representation of the HierarchicalInterview object.

        Returns:
            str: String representation of the interview ID and date.
        """

        return f'interviewId:{self.interviewId} - date: {self.date}'

    def __repr__(self):
        """
        Returns a detailed string representation of the HierarchicalInterview
        object.

        Returns:
            str: Detailed string representation of the interview ID and date.
        """

        return f'interviewId:{self.interviewId} - date: {self.date}'


class Interview:
    """
    Represents an interview.

    Attributes:
        interviewId (str): The unique identifier for the interview.
        date (str): The date of the interview.
        complete (bool): Indicates whether the interview is complete.
        responses (list): A list of VariableData objects representing the
        responses.
        hierarchical_interviews (list): A list of nested HierarchicalInterview
        objects.
    """
    def __init__(self, interviewId="", date="", complete=True, responses=None,
                 hierarchicalInterviews=None):
        """
        Initializes an Interview object.

        Args:
            interviewId (str, optional): The unique identifier for the
            interview. Defaults to an empty string.
            date (str, optional): The date of the interview. Defaults to an
            empty string.
            complete (bool, optional): Indicates whether the interview is
            complete. Defaults to True.
            responses (list, optional): A list of VariableData objects.
            Defaults to None.
            hierarchicalInterviews (list, optional): A list of nested
            HierarchicalInterview objects. Defaults to None.
        """
        self.interviewId = interviewId
        self.date = date
        self.complete = complete
        self.responses = parse(responses, VariableData)
        self.hierarchical_interviews = parse(hierarchicalInterviews,
                                             HierarchicalInterview)

    def __str__(self):
        """
        Returns a string representation of the Interview object.

        Returns:
            str: String representation of the interview ID and date.
        """
        return f'interviewId:{self.interviewId} - date: {self.date}'

    def __repr__(self):
        """
        Returns a detailed string representation of the Interview object.

        Returns:
            str: Detailed string representation of the interview ID and date.
        """
        return f'interviewId:{self.interviewId} - date: {self.date}'

    def to_tsapi(self):
        """
        Converts the Interview object to a dictionary in the TSAPI format.

        Returns:
            dict: Dictionary in the TSAPI format representing the interview.
        """
        _dict = {'interviewId': self.interviewId,
                 'date': self.date,
                 'complete': self.complete,
                 'responses': [di.to_tsapi() for di in self.responses]}
        if self.hierarchical_interviews:
            _dict['hierarchicalInterviews'] = [hi.to_tsapi() for hi in
                                               self.hierarchical_interviews]

        return _dict
