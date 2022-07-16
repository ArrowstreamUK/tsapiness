import xml.etree.ElementTree as et
import tsapiness.tsapi as ts


class Connection:
    def __init__(self, asc_file, sss_file):
        self.asc_file = asc_file
        self.sss_file = sss_file


class Survey:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.metadata = SurveyMetaData(self.connection.sss_file)
        self.interviews = self.get_interviews(self.connection.asc_file)

    def get_interviews(self, file):
        interviews = []
        with open(file) as f:
            lines = f.readlines()
            count_row_id = 0

            for line in lines:
                # create Interview
                count_row_id += 1
                i = {'ident': count_row_id,
                     'date': None,
                     'complete': True,
                     'dataItems': []
                     }
                iv = ts.Interview(**i)

                # populate dataitems
                for loc in self.metadata.variable_positions:
                    start = 0
                    finish = 0
                    subfields = 0
                    width = 0

                    start = int(loc['start']) - 1
                    finish = int(loc['finish'])
                    if 'subfields' in loc.keys():
                        subfields = int(loc['subfields'])
                    else:
                        subfields = 0
                    if 'width' in loc.keys():
                        width = int(loc['width'])
                    else:
                        width = 0
                    datapoint = line[start:finish]
                    datapoints = []
                    if subfields > 0:
                        datapoints = [datapoint[i:i + width] for i in
                                      range(0, len(datapoint), width)]
                    else:
                        datapoints.append(datapoint)

                    di = ts.DataItem(ident=loc['ident'], values=datapoints)
                    iv.data_items.append(di)
                interviews.append(iv)
        return interviews


def _get_node_attrib(item, attribute, if_none):
    _a = if_none
    if attribute in item.attrib:
        _a = item.attrib[attribute]
        return _a


class SurveyMetaData:
    def __init__(self, file):
        self.file = file
        self.tree = et.parse(self.file)
        self.survey = self.get_survey()
        self.variable_positions = self._get_variable_position()

    @property
    def xml_tree(self):
        tree = et.parse(self.file)
        return tree

    def _root(self):
        _root = self.xml_tree.getroot()
        return _root

    def get_value(self, node):
        v_ident = _get_node_attrib(node, 'ident', "")
        v_code = _get_node_attrib(node, 'code', "")
        v_score = _get_node_attrib(node, 'score', 0)
        v_ref = None

        v_label = node.text
        v_label = {'text': v_label}
        _v = ts.Value(label=v_label,
                      ident=v_ident,
                      code=v_code,
                      score=v_score,
                      ref=v_ref)

        return _v

    def get_variable_values(self, node):
        # expects the node called values
        # values can have two types of items 1. range, 2. value
        # there will be only one range but an unlimited number of values.
        if node.tag == 'values':
            _variable_value = ts.VariableValues()
            _range = None
            value_list = []
            for val in node.findall('value'):
                _val = self.get_value(val)
                value_list.append(_val)

            for rng in node.findall('range'):
                range_to = _get_node_attrib(rng, 'to', 0)
                range_from = _get_node_attrib(rng, 'from', 0)
                range_dict = {'from': range_from, 'to': range_to}
                _range = ts.ValueRange(**range_dict)
            _variable_value.values = value_list
            _variable_value.range = _range
            return _variable_value
        else:
            pass

    def get_survey(self):
        survey_node = self._root().findall('survey')[0]
        s_name = ''
        s_title = ''
        for attr in survey_node:
            if attr.tag == 'name':
                s_name = attr.text
            elif attr.tag == 'title':
                s_title = attr.text
        _s = ts.SurveyMetadata(name=s_name, title=s_title)
        _s.variables = self._get_variable()

        return _s

    def _get_variable_position(self):
        variable_nodes = self._root().iter('variable')
        v_list = []
        for var in variable_nodes:
            v_ident = _get_node_attrib(var, 'ident', "")
            v_pos = {}
            v_spread = {}
            v_size = 0

            for attr in var:
                v_pos = attr.attrib if attr.tag == 'position' else v_pos
                v_spread = attr.attrib if attr.tag == 'spread' else v_spread
                v_size = attr.attrib if attr.tag == 'size' else v_size
            v_data_location = {'ident': v_ident}
            v_data_location.update(v_pos)
            v_data_location.update(v_spread)
            if v_size > 0:
                v_data_location.update({'size': v_size})
            v_list.append(v_data_location)
        return v_list

    def _get_variable(self):
        variable_nodes = self._root().iter('variable')
        v_list = []
        for var in variable_nodes:
            v_ident = _get_node_attrib(var, 'ident', "")
            v_type = _get_node_attrib(var, 'type', "").title()
            v_use = _get_node_attrib(var, 'use', "")
            v_label = ""
            v_name = ""
            v_values = None

            for attr in var:
                v_label = attr.text if attr.tag == 'label' else v_label
                v_name = attr.text if attr.tag == 'name' else v_name
                v_values = self.get_variable_values(
                    attr) if attr.tag == 'values' else v_values

            v_label = {'text': v_label}
            _v = ts.Variable(ident=v_ident, type=v_type, use=v_use,
                             label=v_label, name=v_name)

            _v.variable_values = v_values
            v_list.append(_v)
        return v_list

