from db import Select


def parse_args(args):
    filters = dict()
    selects = []
    for arg_name, value in args.items():
        if arg_name.startswith("$"):
            filters[arg_name[1:]] = split_argument_list(value)
        elif str.lower(arg_name) == "select":
            selects = [Select.from_string(select_string) for select_string in split_argument_list(value)]
        else:
            raise ValueError(f'"{arg_name}" is not a valid query parameter')

    return filters, selects


def split_argument_list(arg_list, separator=','):
    return arg_list.replace(" ", "").split(separator)
