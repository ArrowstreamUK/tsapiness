import tsapi_py as ts
from tsapi_py.connectors import connector_tsapi, connector_sss, connector_sav
import pandas as pd
import json
import requests

# Create tsapi object from TSAPI demo server

SERVER = 'https://tsapi-demo.azurewebsites.net'
conn = connector_tsapi.Connection(server=SERVER)
surveys = connector_tsapi.Surveys(connection=conn)
survey_id = surveys[0]['id']
survey_from_api = connector_tsapi.Survey(survey_id=survey_id, connection=conn)

# create tsapi from triple s file:

sss_file = r'C:\example.sss'
asc_file = r'C:\example.asc'

conn = connector_sss.Connection(sss_file=sss_file, asc_file=asc_file)
survey_from_sss = connector_sss.Survey(connection=conn)

# save back to json
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(survey_from_sss.metadata.survey.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)

# create tsapi from sav file

# source:
# https://www.pewresearch.org/global/dataset/2014-spring-global-attitudes/

sav_file = r"C:\Pew Global Attitudes Spring 2014.sav"
conn = connector_sav.Connection(sav_file=sav_file)
survey_from_sav = connector_sav.Survey(connection=conn)



