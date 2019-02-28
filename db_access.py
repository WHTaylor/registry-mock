from db import Table
from enum import Enum


def get_records(table: Table, filters=None):
    all_records = table.get_records()
    if not filters:
        return [record for record in all_records]

    filtered_records = []
    for record in all_records:
        valid = True
        for attribute, value_list in filters.items():
            try:
                if record[attribute] not in value_list:
                    valid = False
                    break
            except KeyError:
                valid = False
                break
        if valid:
            filtered_records.append(record)
    return filtered_records


def get_next_id(table: Table):
    return len(table.get_records()) + 1


schema = {
    Table.PROPOSAL: [
        "reference_number",
        "facility",
        "access_route",
        "title",
        "round",
        "pi_un",
        "created",
        "note",
        "org_id"],
    Table.ALLOCATION: [
        "allocated_time",
        "allocated_instrument"
    ],
    Table.REQUEST: [
        "requested_time",
        "requested_instrument",
        "alternative_instruments"
    ],
    Table.FAP: [
        "panel",
        "score",
        "feedback"
    ]
}

reverse_schema = {
    e: k for k, v in schema.items() for e in v
}


class ProposalSubsection(Enum):
    REQUEST = Table.REQUEST
    ALLOCATION = Table.ALLOCATION
    FAP = Table.FAP
    CORE = None
    CONTACTS = [(Table.PROPOSAL_TO_CONTACT, 'contact_id', 'id'), Table.CONTACT]

    @staticmethod
    def from_string(s):
        if str.lower(s) == "request":
            return ProposalSubsection.REQUEST
        elif str.lower(s) == "allocation":
            return ProposalSubsection.ALLOCATION
        elif str.lower(s) == "fap":
            return ProposalSubsection.FAP
        elif not s or str.lower(s) == "core" or str.lower(s) == "none":
            return ProposalSubsection.CORE
        elif str.lower(s) == "contacts":
            return ProposalSubsection.CONTACTS
        else:
            raise ValueError(f'"{s}" is not a subsection of a proposal')

    def get_data(self, filters):
        if self.value in Table:
            return get_records(self.value, filters)
        elif self.value is None:
            return []
        else:
            # This definitely won't work in the general case (more than one join), and is probably full of bugs.
            # Hacked together to get something a bit like table joins 'working'
            id_mapping = {}
            original_filter_key_name = list(filters.keys())[0]
            for (join_table, next_id_cur_table, next_id_next_table) in self.value[:-1]:
                records = get_records(join_table, filters)
                for record in records:
                    v = id_mapping.get(record[original_filter_key_name], [])
                    v.append(record[next_id_cur_table])
                    id_mapping[record[original_filter_key_name]] = v
                filters = {next_id_next_table: set([e[next_id_cur_table] for e in records])}
            records = get_records(self.value[-1], filters)
            final_records = []
            for record in records:
                for original_id, final_record_ids in id_mapping.items():
                    if record['id'] in final_record_ids:
                        record_copy = {k: v for k, v in record.items()}
                        record_copy[original_filter_key_name] = original_id
                        final_records.append(record_copy)
            return final_records
