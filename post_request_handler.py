from db import Table
import db_access


required_fields = [
    'reference_number',
    'facility',
    'access_route',
    'title',
    'round',
    'pi_un',
    'org_id'
]


def create_proposal(request_json):
    validate_request(request_json)
    proposal_core = {
        field: request_json[field] for field in required_fields
    }
    proposal_core['note'] = request_json.get('note', None)
    proposal_core['id'] = db_access.get_next_id(Table.PROPOSAL)
    return [Table.PROPOSAL.insert_record(proposal_core)]


def validate_request(request_json):
    if not request_json:
        raise ValueError("No data sent by POST request")

    for field in required_fields:
        if field not in request_json:
            raise ValueError(f"Required field '{field}' missing when trying to create a proposal")
