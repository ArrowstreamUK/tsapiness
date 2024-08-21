import pandas as pd
import pyreadstat

import tsapiness.tsapi as ts


class Connection:
    def __init__(self, sav_file):
        self.sav_file = sav_file


class Survey:

    def __init__(self, connection: Connection):
        self.connection = connection
        self.data, self.meta = pyreadstat.read_sav(self.connection.sav_file)
        self.metadata = self.get_metadata(self.meta)
        self.interviews = self.get_interviews(self.data)

    def check_range(self, vi):
        d = self.data[vi]

        v_max = d.values.max()
        v_min = d.values.min()
        value_range_dict = {'from': v_min, 'to': v_max}
        _r = ts.ValueRange(**value_range_dict)
        return _r

    def get_interviews(self, data):
        interviews = []
        raw_interview = pd.DataFrame(data)

        for index, row in raw_interview.iterrows():
            _dict = {'interviewId': row.ID,
                     'date': "",
                     'complete': True,
                     'responses': []}
            interview = ts.Interview(**_dict)

            for name, value in row.items():
                if not pd.isna(value):
                    di = ts.VariableData(variableId=name,
                                         data=[{'value': value}])
                    interview.responses.append(di)
            interviews.append(interview)

        return interviews

    def get_metadata(self, data):

        s_name = str(self.connection.sav_file).split('\\')[-1]
        s_title = ''
        _s = ts.SurveyMetadata(name=s_name, title=s_title)
        _s.variables = self.get_variables()

        return _s

    def get_variables(self):
        number_of_variables = self.meta.number_columns
        m = self.meta
        v_list = []

        for index in range(number_of_variables):

            v_id = m.column_names[index]

            v_type = "single"
            v_use = ""
            v_l = {'text': m.column_names_to_labels[v_id],
                   'altLabels': [{"mode": "interview",
                                  "text": m.column_names_to_labels[v_id],
                                  'languageId': 'EN'}]}
            v_name = ""

            _v = ts.Variable(variableId=v_id, type=v_type, use=v_use,
                             label=v_l, name=v_name)

            if v_id in m.variable_value_labels:
                # do stuff
                values = []
                for key, value in m.variable_value_labels[v_id].items():
                    value_item = ts.Value(valueId=key,
                                          code=key,
                                          label={'text': value})

                    values.append(value_item)

                _v.variable_values.values = values
            # value_range = self.check_range(v_id)
            # _v.variable_values.range = value_range
            v_list.append(_v)
        return v_list
