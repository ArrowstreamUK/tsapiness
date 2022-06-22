# TSAPI-py

The TSAPI-py aims to make the TSAPI easy to access via Python. 

Currently the project provides a python representation of the TSAPI so that the data can be manipulated accordingly. 
More details on TSAPI can be found here. 
https://www.tsapi.net/

These are early days for the project but the aim is to create a PYPI package that other applications can rely on. 

A simple implementation is below...

```
import tsapi as ts
import pandas as pd

# Access the TSAPI demp server
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

```
