import xml.etree.ElementTree as ET
import tsapi as ts


def get_node_attrib(item, attribute, if_none):
    _a = if_none
    if attribute in item.attrib:
        _a = item.attrib[attribute]
        return _a


def get_value(node):
    v_ident = get_node_attrib(node, 'ident', "")
    v_code = get_node_attrib(node, 'code', "")
    v_score = get_node_attrib(node, 'score', 0)
    v_ref = None

    v_label = node.text
    v_label = {'text': v_label}
    _v = ts.Value(label=v_label,
                  ident=v_ident,
                  code=v_code,
                  score=v_score,
                  ref=v_ref)

    return _v


def get_variable_values(node):
    # expects the node called values
    # values can have two types of items 1. range, 2. value
    # there will be only one range but an unlimited number of values.
    if node.tag == 'values':
        _variable_value = ts.VariableValues()
        _range = None
        value_list = []
        for val in node.findall('value'):
            _val = get_value(val)
            value_list.append(_val)

        for rng in node.findall('range'):
            range_to = get_node_attrib(rng, 'to', 0)
            range_from = get_node_attrib(rng, 'from', 0)
            range_dict = {'from': range_from, 'to': range_to}
            _range = ts.ValueRange(**range_dict)
        _variable_value.values = value_list
        _variable_value.range = _range
        return _variable_value
    else:
        pass


class TripleS:
    def __init__(self, file):
        self.file = file
        self.tree = ET.parse(self.file)
        self.survey = None

    @property
    def xml_tree(self):
        tree = ET.parse(self.file)
        return tree

    def _root(self):
        _root = self.xml_tree.getroot()
        return _root

    def get_survey(self):
        survey_node = self._root().findall('survey')[0]
        s_name = ''
        s_title = ''
        for attr in survey_node:
            if attr.tag == 'name':
                s_name = attr.text
            elif attr.tag == 'title':
                s_title = attr.text
        _s = ts.Survey(name=s_name, title=s_title)
        _s.variables = self._get_variable()
        return _s

    def _get_variable(self):
        variable_nodes = self._root().iter('variable')
        v_list = []
        for var in variable_nodes:
            v_ident = get_node_attrib(var, 'ident', "")
            v_type = get_node_attrib(var, 'type', "").title()
            v_use = get_node_attrib(var, 'use', "")
            v_label = ""
            v_name = ""
            v_values = None

            for attr in var:
                v_label = attr.text if attr.tag == 'label' else v_label
                v_name = attr.text if attr.tag == 'name' else v_name
                v_values = get_variable_values(
                    attr) if attr.tag == 'values' else v_values

            # v_pos = var.text if var.tag == 'position' else v_pos
            # v_size = var.text if var.tag == 'size' else v_size
            v_label = {'text': v_label}
            _v = ts.Variable(ident=v_ident, type=v_type, use=v_use,
                             label=v_label, name=v_name)
            _v.variable_values = v_values
            v_list.append(_v)
        return v_list

# f = r'C:\Users\alebr\Desktop\WI.sss'
#
# sss = TripleS(f)


