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
