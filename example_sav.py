import tsapiness as ts
import json


# create tsapi from sav file:
sav_file = r'C:\Users\alebr\PycharmProjects\tsapiness\data\Pew Research Global Attitudes Spring 2018 Dataset WEB FINAL.sav'
conn = ts.connector_sav.Connection(sav_file=sav_file)

survey_from_sav = ts.connector_sav.Survey(connection=conn)

# save back to json
survey_to_export = survey_from_sav


with open(r'data/metadata_sav.json', 'w', encoding='utf8') as f:
    json.dump(survey_to_export.metadata.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)
with open(r'data/data_sav.json', 'w', encoding='utf8') as f:
    json.dump([interview.to_tsapi()
               for interview in survey_to_export.interviews][0],
              f,
              indent=4,
              ensure_ascii=False)
