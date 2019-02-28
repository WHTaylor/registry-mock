from db import Table
import db_access
from datetime import datetime


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
    proposal_core['created'] = datetime.now()

    additional_records_to_insert = {}
    for field, value in request_json.items():
        if field not in db_access.schema[Table.PROPOSAL]:
            try:
                table = db_access.reverse_schema[field]
                record_for_table = additional_records_to_insert.get(table, {})
                record_for_table[field] = value
                additional_records_to_insert[table] = record_for_table
            except KeyError:
                raise ValueError(f'"{field}" is not a valid field for creating a proposal"')

    for table, record in additional_records_to_insert.items():
        record['proposal_id'] = proposal_core['id']
        record['id'] = db_access.get_next_id(table)
        table.insert_record(record)

    return [Table.PROPOSAL.insert_record(proposal_core)]


def validate_request(request_json):
    if not request_json:
        raise ValueError("No data sent by POST request")

    for field in required_fields:
        if field not in request_json:
            raise ValueError(f"Required field '{field}' missing when trying to create a proposal")
