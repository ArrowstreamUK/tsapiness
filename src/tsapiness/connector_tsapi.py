import json
import requests
import tsapiness.tsapi as ts


class Connection:
    def __init__(self, server):
        self.server = server


class Surveys:
    def __init__(self, connection):
        self.connection = connection
        self.surveys = self.get_surveys()

    def __getitem__(self, item):
        return self.surveys[item]

    def __iter__(self):
        return list(self.surveys)

    def __next__(self):
        try:
            result = self.surveys[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def get_surveys(self):
        r = requests.get(f'{self.connection.server}/Surveys')
        a = json.loads(r.text)
        return a


class Survey:
    def __init__(self, survey_id, connection):
        self.connection = connection
        self.metadata = self.get_survey(survey_id)
        self.interviews = self.get_interviews(survey_id)

    def get_survey(self, s_id):
        url = f'{self.connection.server}/Surveys/{s_id}/Metadata'
        r = requests.get(url)
        json_r = json.loads(r.text)
        survey_obj = ts.SurveyMetadata(**json_r)

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
            f'{self.connection.server}/Surveys/Interviews',
            headers=headers, json=json_data)
        json_r = json.loads(r.text)
        interviews = []
        for interview in json_r:
            interview_record = ts.Interview(**interview)
            interviews.append(interview_record)

        return interviews
