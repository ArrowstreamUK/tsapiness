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

with open('data.json', 'w', encoding='utf8') as f:
    json.dump(survey_from_sss.survey.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)
