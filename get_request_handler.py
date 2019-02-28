from db_access import get_records
from db import Table


def get_proposals(filters=None, selects=None):
    return get_records(Table.PROPOSAL, filters)
