import json
import logging
import requests
from time import sleep
from typing import Optional

from datasets import Dataset
from pydantic import BaseModel

from chaiverse.http_client import DataClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PreferenceData(BaseModel):
    submission_id: str
    data_name: Optional[str]

    @classmethod
    def from_submission_id(cls, submission_id):
        preference_data = cls(submission_id=submission_id)
        preference_data.data_name = DataClient().get(f'/v1/big_data/submission_preferences/{submission_id}')
        return preference_data

    def generate(self, max_hours=7 * 24.0, limit=100000, public_only=True):
        params = dict(max_hours=max_hours, limit=limit, public_only=public_only)
        self.data_name = DataClient().post(f'/v1/big_data/submission_preferences/{self.submission_id}', params=params)
        return self

    def get_job_status(self):
        status = None
        if self.data_name:
            params = dict(job_id=self.data_name)
            status = DataClient().get(f'/v1/big_data/job_status', params=params)
            return status
        return status

    def get_download_link(self):
        if not self.data_name:
            print('Please call generate to trigger generation of preference data.')
            download_link = None
        else:
            download_link = self._get_download_link()
        return download_link

    def load_dataset(self):
        download_link = self.get_download_link()
        ds = None
        if download_link:
            response = requests.get(download_link)
            lines = response.text.splitlines()
            dicts = [json.loads(line) for line in lines]
            ds = Dataset.from_list(dicts)
        return ds

    def _get_download_link(self):
        while True:
            status = self.get_job_status()
            has_completed = status['has_completed']
            print(f'Job={self.data_name} status={status}')
            if has_completed:
                break
            sleep(5)
        download_link = DataClient().get(f'/v1/big_data/get_download_link/{self.data_name}')
        return download_link
