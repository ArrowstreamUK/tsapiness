import tsapiness as ts
import json

sss_file = 'data/example.sss'
asc_file = 'data/example.asc'

conn = ts.connector_sss.Connection(sss_file=sss_file, asc_file=asc_file)
survey_from_sss = ts.connector_sss.Survey(connection=conn)

with open('data/metadata_sss.json', 'w', encoding='utf8') as f:
    json.dump(survey_to_export.metadata.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)
with open('data/data_sss.json', 'w', encoding='utf8') as f:
    json.dump([interview.to_tsapi()
               for interview in survey_to_export.interviews],
              f,
              indent=4,
              ensure_ascii=False)