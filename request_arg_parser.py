from db_access import ProposalSubsection


def parse_args(args):
    filters = dict()
    subsections = []
    for arg_name, value in args.items():
        if arg_name.startswith("$"):
            filters[arg_name[1:]] = split_argument_list(value)
        elif str.lower(arg_name) == "select":
            subsections = [ProposalSubsection.from_string(subsection) for subsection in split_argument_list(value)]
        else:
            raise ValueError(f'"{arg_name}" is not a valid query parameter')

    return filters, subsections


def split_argument_list(arg_list, separator=','):
    return arg_list.replace(" ", "").split(separator)
