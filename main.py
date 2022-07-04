import tsapi_py as ts
from tsapi_py.connectors import connector_tsapi, connector_sss
import pandas as pd
import json
import requests

# Access the TSAPI demo server


SERVER = 'https://tsapi-demo.azurewebsites.net'
conn = connector_tsapi.Connection(server=SERVER)

surveys = connector_tsapi.Surveys(connection=conn)

survey_id = surveys[0]['id']
survey_from_api = connector_tsapi.Survey(survey_id=survey_id, connection=conn)


# now apply method for flattening the survey into a tabular format.

# example of exporting to csv
data_rows = []

for section in survey_from_api.metadata.sections:
    for v in section.variables:
        data_rows = ts.tsapi.flatten_variable(variable=v,
                                              variable_list=data_rows)
df = pd.DataFrame(data_rows)
df.to_csv('meta.csv', index=False)

# create tsapi from triple s file:

sss_file = r'C:\training data.sss'
asc_file = r'C:\Askia Training Data.asc'


conn = connector_sss.Connection(sss_file=sss_file, asc_file=asc_file)
survey_from_sss = connector_sss.Survey(connection=conn)


# sss.survey = sss.get_survey()


# with open(f_data) as f:
#     lines = f.readlines()
#     count_row_id = 0
#     interviews = []
#
#     for l in lines:
#         # create Interview
#         count_row_id += 1
#         i = {'ident': count_row_id,
#              'date': None,
#              'complete': True,
#              'dataItems': []
#              }
#         iv = ts.tsapi.Interview(**i)
#
#         # populate dataitems
#         for loc in ss.meta_data.variable_positions:
#             start = 0
#             finish = 0
#             subfields = 0
#             width = 0
#
#             start = int(loc['start'])-1
#             finish = int(loc['finish'])
#             if 'subfields' in loc.keys():
#                 subfields = int(loc['subfields'])
#             else:
#                 subfields = 0
#             if 'width' in loc.keys():
#                 width = int(loc['width'])
#             else:
#                 width = 0
#             datapoint = l[start:finish]
#             datapoints = []
#             if subfields > 0:
#                 datapoints = [datapoint[i:i + width] for i in range(0, len(datapoint), width)]
#             else:
#                 datapoints.append(datapoint)
#
#             di = ts.tsapi.DataItem(ident=loc['ident'], values=datapoints)
#             iv.data_items.append(di)
#         interviews.append(iv)

with open('data.json', 'w', encoding='utf8') as f:
    json.dump(sss.survey.to_tsapi(), f, indent=4, ensure_ascii=False)
