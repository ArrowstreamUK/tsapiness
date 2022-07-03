import json
import requests
from tsapi_py import tsapi


class connection:
    def __init__(self, server):
        self.server = server

class Surveys:
    def __init__(self, connection):
        self.surveys = self.get_surveys()


    def get_surveys(self):
        r = requests.get(f'{self.server}/Surveys')
        a = json.loads(r.text)
        return a


class Survey:
    def __init__(self, survey_id, connection):

        self.metadata = self.get_interviews(survey_id)
        self.interviews = survey_id

    def get_survey(self, s_id):
        url = f'{self.server}/Surveys/{s_id}/Metadata'
        r = requests.get(url)
        json_r = json.loads(r.text)
        survey_obj = tsapi.SurveyMetadata(**json_r)

        return survey_obj

    def get_interviews(self, s_id):
        headers = {
            'accept': 'application/json',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
        }

        json_data = {
            'surveyId': s_id,
            'start': 1,
            'maxLength': 100,
            'completeOnly': True,
            'date': '2022-06-01T13:19:58.293Z',
        }

        r = requests.post(
            f'{self.server}/Surveys/Interviews',
            headers=headers, json=json_data)
        json_r = json.loads(r.text)
        interviews = []
        for interview in json_r:
            interview_record = tsapi.Interview(**interview)
            interviews.append(interview)

        return interview
