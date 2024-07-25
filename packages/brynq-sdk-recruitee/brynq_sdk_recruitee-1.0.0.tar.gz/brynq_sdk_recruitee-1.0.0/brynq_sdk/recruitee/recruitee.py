import pandas as pd
import requests
from typing import Union, List
from brynq_sdk.brynq import BrynQ

class Recruitee(BrynQ):
    """
    This class is meant to be a simple wrapper around the Recruitee API. In order to start using it, authorize your application in BrynQ.
    You will need to provide a token for the authorization, which can be set up in BrynQ and referred to with a label.
    Besides, you need to add a company ID which can be provided by the customer.
    You can find the Recruitee API here: https://api.recruitee.com/docs/index.html
    """
    def __init__(self, label: Union[str, List], api_type: str = "API"):
        super().__init__()
        credentials = self.get_system_credential(system='recruitee', label=label)
        self.url = f'https://api.recruitee.com/c/{credentials["company_id"]}/'
        self.headers = {"Authorization": f"Bearer {credentials['token']}",
                        "Content-Type": "application/json"}

    def get_candidates(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the candidates data from Recruitee
        :param filters: A dict with filters. See the Recruitee API docs for more info: https://api.recruitee.com/docs/index.html#candidate.web.candidate-candidate.web.candidate-get
        :return:
        """
        response = requests.get(url=f"{self.url}candidates",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        return response

    def get_mailbox(self, candidate_id: str = None) -> pd.DataFrame:
        """
        This method retrieves the mailbox data from Recruitee.
        :return:
        """
        response = requests.get(url=f"{self.url}mailbox/candidate/{candidate_id}",
                                headers=self.headers)
        response.raise_for_status()
        return response
