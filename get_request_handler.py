from db_access import get_records
from db import Table, Select


def get_proposals(filters=None, selects=None):
    selected_proposals = get_records(Table.PROPOSAL, filters)
    proposal_ids = [proposal['id'] for proposal in selected_proposals]
    if not selects:
        selects = [s for s in Select]
    for select in selects:
        matching_sub_selects = get_records(select.value, {'proposal_id': proposal_ids})
        selected_proposals = append_extra_fields(selected_proposals, matching_sub_selects, str.lower(select.name))
    return selected_proposals


def append_extra_fields(proposals, extra_field_objects, embedded_name, dont_flatten=False):
    ids_to_proposals = {proposal['id']: proposal for proposal in proposals}
    ids_to_extra_fields = {}
    for proposal_id in ids_to_proposals:
        for extra_fields in extra_field_objects:
            if extra_fields['proposal_id'] == proposal_id:
                v = ids_to_extra_fields.get(proposal_id, [])
                v.append(extra_fields)
                ids_to_extra_fields[proposal_id] = v

    if ids_to_extra_fields:
        embed = dont_flatten or max([len(v) for v in ids_to_extra_fields.values()]) > 1
        for proposal_id, field_objects_to_add in ids_to_extra_fields.items():
            if embed:
                for fields_to_add in field_objects_to_add:
                    embed_fields(embedded_name, fields_to_add, ids_to_proposals[proposal_id])
            else:
                for k, v in field_objects_to_add[0].items():
                    if non_id_key(k):
                        ids_to_proposals[proposal_id][k] = v

    return [proposal for proposal in ids_to_proposals.values()]


def embed_fields(embed_name, fields, parent):
    embed_object = {k: v for k, v in fields.items() if non_id_key(k)}
    v = parent.get(embed_name, [])
    v.append(embed_object)
    parent[embed_name] = v


def non_id_key(k):
    return k != 'proposal_id' and k != 'id'
