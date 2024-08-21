from tsapiness.connector_tsapi import Connection, Surveys, Survey

import json

# Create tsapi object from TSAPI demo server

SERVER = 'https://tsapi-demo.azurewebsites.net'
conn = ts.connector_tsapi.Connection(server=SERVER)
surveys = ts.connector_tsapi.Surveys(connection=conn)
survey_id = surveys[0]['id']
survey_from_api = ts.connector_tsapi.Survey(survey_id=survey_id,
                                            connection=conn)


survey_to_export = survey_from_api


with open('data/metadata_api.json', 'w', encoding='utf8') as f:
    json.dump(survey_from_api.metadata.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)
with open('data/data_api.json', 'w', encoding='utf8') as f:
    json.dump([interview.to_tsapi()
               for interview in survey_from_api.interviews],
              f,
              indent=4,
              ensure_ascii=False)
