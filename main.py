import tsapi as ts
import pandas as pd

# Access the TSAPI demo server
ts.SERVER = 'https://tsapi-demo.azurewebsites.net'

# get list of all available surveys on server
surveys = ts.get_surveys()

# select first survey on server and source the json
survey = surveys[0]
r = ts.get_survey_detail_json(survey['id'])

# create the survey object
s = ts.get_survey(r)

# now apply method for flattening the survey into a tabular format.

data_rows = []
for section in s.sections:
    for v in section.variables:
        data_rows = ts.flatten_variable(variable=v,
                                        variable_list=data_rows)

df = pd.DataFrame(data_rows)
df.to_csv('meta.csv', index=False)

