from db import Table


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


def get_next_id(table):
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
