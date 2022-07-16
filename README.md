# tsapiness

tsapiness (pronounced "zappiness") aims to make the TSAPI easy to access via Python. 

Currently, the project provides a python representation of the TSAPI so that the data can be manipulated accordingly. 
More details on TSAPI can be found here. 
https://www.tsapi.net/

These are early days for the project, in this early version you can:
* convert an SPSS sav file to tsapi format
* convert a triple-s file to tsapi format
* read tsapi from a webserver

Future development intends to:
* convert other survey platform APIs to the tsapi format
* provide tools for converting flat tsapi structures that occur when importing from sav or triple-s into the more native hierarchical tsapi structure
* provide full documentation on how to use tsapiness effectively. 

A simple implementation is below...

```


import tsapiness as ts
import json

# Create tsapi object from TSAPI demo server

SERVER = 'https://tsapi-demo.azurewebsites.net'
conn = ts.connector_tsapi.Connection(server=SERVER)
surveys = ts.connector_tsapi.Surveys(connection=conn)
survey_id = surveys[0]['id']
survey_from_api = ts.connector_tsapi.Survey(survey_id=survey_id, connection=conn)

# create tsapi from triple s file:

sss_file = '../data/example.sss'
asc_file = '../data/example.asc'

conn = ts.connector_sss.Connection(sss_file=sss_file, asc_file=asc_file)
survey_from_sss = ts.connector_sss.Survey(connection=conn)

# save back to json
with open('../data/data.json', 'w', encoding='utf8') as f:
    json.dump(survey_from_sss.metadata.survey.to_tsapi(),
              f,
              indent=4,
              ensure_ascii=False)

# create tsapi from sav file

# source:
# https://www.pewresearch.org/global/dataset/2014-spring-global-attitudes/

sav_file = '../data/Pew Global Attitudes Spring 2014.sav'
conn = ts.connector_sav.Connection(sav_file=sav_file)
survey_from_sav = ts.connector_sav.Survey(connection=conn)

```