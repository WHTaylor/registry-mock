def parse_args(args):
    filter_keys = []
    filter_vals = []
    selects = []
    for arg_name, value in args.items():
        if str.lower(arg_name) == "filter_keys":
            filter_keys = split_argument_list(value)
        elif str.lower(arg_name) == "filter_values":
            filter_vals = split_argument_list(value)
        elif str.lower(arg_name) == "select":
            selects = split_argument_list(value)
        else:
            raise ValueError(f'"{arg_name}" is not a valid query parameter')

    if filter_keys and filter_vals:
        if len(filter_keys) != len(filter_vals):
            raise ValueError(f'Must have a matching number of filter keys and values')

    return dict(zip(filter_keys, filter_vals)), selects


def split_argument_list(arg_list, separator=','):
    return arg_list.replace(" ", "").split(separator)
