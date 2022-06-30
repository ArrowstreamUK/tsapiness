import json
import requests
from tsapi_py import tsapi


class SurveyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class TSAPIServer:
    def __init__(self, server):
        self.server = server
        self.surveys = self.get_surveys()
        self.survey = []

    def get_surveys(self):
        r = requests.get(f'{self.server}/Surveys')
        a = json.loads(r.text)
        return a

    def get_survey(self, s_id):
        url = f'{self.server}/Surveys/{s_id}/Metadata'
        r = requests.get(url)
        json_r = json.loads(r.text)
        survey_obj = tsapi.Survey(**json_r)

        return survey_obj