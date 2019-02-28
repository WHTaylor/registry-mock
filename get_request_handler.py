from db_access import get_records
from db import Table, Select


def append_extra_fields(proposals, extra_field_objects, embedded_name):
    for proposal in proposals:
        for extra_fields in extra_field_objects:
            if extra_fields['proposal_id'] == proposal['id']:
                embed = {k: v for k, v in extra_fields.items() if k != 'proposal_id'}
                proposal[embedded_name] = embed
    return proposals


def get_proposals(filters=None, selects=None):
    selected_proposals = get_records(Table.PROPOSAL, filters)
    proposals_ids = [proposal['id'] for proposal in selected_proposals]
    if not selects:
        selects = [s for s in Select]
    for select in selects:
        matching_sub_selects = get_records(select.value, {'proposal_id': proposals_ids})
        selected_proposals = append_extra_fields(selected_proposals, matching_sub_selects, select.name)
    return selected_proposals
