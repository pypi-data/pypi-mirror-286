import requests

from .helpers import check_valid_param
from . import config

class Client:
    def __init__(
            self,
            base_url=config.BASE_URL
        ):

        self.base_url = base_url

    def request(self, endpoint, params=None, headers=None, payload=None, http_method='GET'):
        if not params:
            params = {}

        if not headers:
            headers = {}

        if not payload:
            payload = {}

        url = self.base_url + endpoint
        
        r = requests.request(method=http_method, url=url, headers=headers, params=params, data=payload)
        
        if r.status_code == 200:
            try:
                return r.json()
            except requests.exceptions.JSONDecodeError as e:
                raise requests.exceptions.JSONDecodeError(f'Encountered status code {r.status_code}. See response below.\n\n{r.text}', e.doc, e.pos)
            
    def get_all_people(
            self,
            id=None, 
            political_affiliation=None, # One of REPUBLICAN, DEMOCRAT, or INDEPENDENT
            role=None, # One of CONGRESS, SENATE, VICE_PRESIDENT, or PRESIDENT
            status=None, # One of RUNNING_FOR or HELD
            primary_state=None, # A state abbreviation (e.g. IL, OK, NY, etc.)
        ):
        all_people = self.request('/api/public/dtsi/all-people')

        if id:
            check_valid_param(id, 'id', valid_type=str)
            all_people['people'] = list(filter(lambda x: x['id'] == id, all_people['people']))

        if political_affiliation:
            political_affiliation = political_affiliation.upper()
            check_valid_param(political_affiliation, 'political_affiliation', valid_values=config.VALID_POLITICAL_AFFILIATIONS, valid_type=str)
            all_people['people'] = list(filter(lambda x: x['politicalAffiliationCategory'] == political_affiliation, all_people['people']))
        
        if role:
            role = role.upper()
            check_valid_param(role, 'role', valid_values=config.VALID_ROLES, valid_type=str)
            all_people['people'] = list(filter(lambda x: x['primaryRole']['roleCategory'] == role, all_people['people']))

        if status:
            status = status.upper()
            check_valid_param(status, 'status', valid_values=config.VALID_STATUSES, valid_type=str)
            all_people['people'] = list(filter(lambda x: x['primaryRole']['status'] == status, all_people['people']))
        
        if primary_state:
            check_valid_param(primary_state, 'primary_state', valid_type=str)
            all_people['people'] = list(filter(lambda x: x['primaryRole']['primaryState'] == primary_state, all_people['people']))

        return all_people