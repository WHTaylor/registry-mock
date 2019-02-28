import json
import os

db_dir = os.path.join(os.curdir, 'db')


def write_db_table(table_name, data):
    file_name = os.path.join(db_dir, table_name + ".json")
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, default=str)


def read_db_table(table_name):
    with open(os.path.join(db_dir, f'{table_name}.json'), 'r') as infile:
        return json.load(infile)


if __name__ == "__main__":
    from db import Table
    for table in Table:
        write_db_table(str.lower(table.name), table._get_db_table())
