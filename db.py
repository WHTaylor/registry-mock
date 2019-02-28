from datetime import datetime
from enum import Enum, auto
from copy import deepcopy


proposals = [
    {"id": 1,
     "reference_number": "1912345",
     "facility": "isis",
     "access_route": "Direct access",
     "title": "My First Proposal",
     "round": "2019_1",
     "pi_un": "1234",
     "created": datetime(2018, 6, 20),
     "note": None,
     "org_id": "this might not even be here"},
    {"id": 2,
     "reference_number": "1912374",
     "facility": "isis",
     "access_route": "Direct access",
     "title": "An allocated ISIS proposal",
     "round": "2019_1",
     "pi_un": "1234",
     "created": datetime(2018, 6, 23),
     "note": None,
     "org_id": "this might not even be here"},
    {"id": 3,
     "reference_number": "1823456",
     "facility": "clf",
     "access_route": "Direct access",
     "title": "An allocated CLF proposal",
     "round": "2018_2",
     "pi_un": "4321",
     "created": datetime(2017, 3, 21),
     "note": "A note",
     "org_id": "this might not even be here"}
]

requests = [
    {"id": 1,
     "proposal_id": 1,
     "requested_time": 3,
     "requested_instrument": "WISH",
     "alternative_instruments": None},
    {"id": 2,
     "proposal_id": 2,
     "requested_time": 2,
     "requested_instrument": "ZOOM",
     "alternative_instruments": None},
    {"id": 3,
     "proposal_id": 3,
     "requested_time": 2,
     "requested_instrument": "LSF",
     "alternative_instruments": None}
]

allocations = [
    {"id": 1,
     "proposal_id": 2,
     "allocated_time": 2,
     "allocated_instrument": "WISH"},
    {"id": 2,
     "proposal_id": 3,
     "allocated_time": 1,
     "allocated_instrument": "LSF"}
]

faps = [
    {"id": 1,
     "proposal_id": 1,
     "panel": 3,
     "score": None,
     "feedback": None},
    {"id": 2,
     "proposal_id": 2,
     "panel": 3,
     "score": 8.5,
     "feedback": None},
    {"id": 3,
     "proposal_id": 3,
     "panel": 8,
     "score": 8,
     "feedback": "one week should be enough"}
]

proposals_to_contacts = [
    {"proposal_id": 1,
     "contact_id": 33},
    {"proposal_id": 2,
     "contact_id": 33},
    {"proposal_id": 3,
     "contact_id": 44},
    {"proposal_id": 3,
     "contact_id": 52}
]

contacts = [
    {"id": 33,
     "un": "321",
     "role": "local contact"},
    {"id": 44,
     "un": "432",
     "role": "local contact"},
    {"id": 52,
     "un": "765",
     "role": "experiment contact"}
]


class Table(Enum):
    PROPOSAL = auto()
    REQUEST = auto()
    ALLOCATION = auto()
    FAP = auto()
    CONTACT = auto()
    PROPOSAL_TO_CONTACT = auto()

    def _get_db_table(self):
        if self.name == 'PROPOSAL':
            return proposals
        elif self.name == 'REQUEST':
            return requests
        elif self.name == 'ALLOCATION':
            return allocations
        elif self.name == 'FAP':
            return faps
        elif self.name == 'CONTACT':
            return contacts
        elif self.name == 'PROPOSAL_TO_CONTACT':
            return proposals_to_contacts

    def get_records(self):
        return deepcopy(self._get_db_table())

    def insert_record(self, record):
        table = self._get_db_table()
        table.append(record)
        return deepcopy(table[-1])
