import tsapi_py as ts
import pandas as pd
import json
# Access the TSAPI demo server
from tsapi_py.connectors import connector_tsapi, connector_sss

SERVER = 'https://tsapi-demo.azurewebsites.net'

api = connector_tsapi.TSAPIServer(server=SERVER)
survey_id = api.surveys[0]['id']
survey_from_api = api.get_survey(s_id=survey_id)

# now apply method for flattening the survey into a tabular format.

# example of exporting to csv
data_rows = []
for section in survey_from_api.sections:
    for v in section.variables:
        data_rows = ts.tsapi.flatten_variable(variable=v,
                                        variable_list=data_rows)
df = pd.DataFrame(data_rows)
df.to_csv('meta.csv', index=False)

# create tsapi from triple s file:

f = r'C:\training data.sss'
sss = connector_sss.TripleS(f)
sss.survey = sss.get_survey()

with open('data.json', 'w', encoding='utf8') as f:
    json.dump(sss.survey.to_tsapi(), f, indent=4, ensure_ascii=False)
