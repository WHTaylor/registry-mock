from db_access import get_records
from db import Table, ProposalSubsection


def get_proposals(filters=None, subsections=None):
    selected_proposals = get_records(Table.PROPOSAL, filters)
    proposal_ids = [proposal['id'] for proposal in selected_proposals]
    if not subsections:
        subsections = [s for s in ProposalSubsection]
    for subsection in subsections:
        if subsection != ProposalSubsection.CORE:
            matching_subsections = get_records(subsection.value, {'proposal_id': proposal_ids})
            selected_proposals = append_extra_fields(selected_proposals, matching_subsections, str.lower(subsection.name))
    return selected_proposals


def append_extra_fields(proposals, subsection_objects, embedded_name, dont_flatten=False):
    ids_to_proposals = {proposal['id']: proposal for proposal in proposals}
    fields_to_append_to_proposals = {}
    for proposal_id in ids_to_proposals:
        for subsection_object in subsection_objects:
            if subsection_object['proposal_id'] == proposal_id:
                v = fields_to_append_to_proposals.get(proposal_id, [])
                v.append(subsection_object)
                fields_to_append_to_proposals[proposal_id] = v

    if fields_to_append_to_proposals:
        embed = dont_flatten or max([len(v) for v in fields_to_append_to_proposals.values()]) > 1
        for proposal_id, field_objects_to_add in fields_to_append_to_proposals.items():
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
