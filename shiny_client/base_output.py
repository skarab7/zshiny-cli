from prettytable import PrettyTable


def print_item(parsed_args, item, fields):
        if parsed_args.is_machine_readable:
            print_machine_readable_item(item, fields)
        else:
            output = get_pretty_table_for_item(item, fields)
            print(output)


def print_machine_readable_item(item, output_fields):

    attrs = _filter_attributes(item.get_attributes(), output_fields)

    for attr in attrs:
        row = []
        row.append(attr)
        row.append(str(getattr(item, attr)))
        print(",".join(row))


def _filter_attributes(attrs, output_fields):
    return [attr for attr in attrs
            if _should_attr_be_printed(output_fields, attr)]


def _should_attr_be_printed(output_fields, attr):
        return "all" in output_fields or attr in output_fields


def get_pretty_table_for_item(item, output_fields):
    """
    """
    x = PrettyTable(["Attribute", "Value"])
    attrs = _filter_attributes(item.get_attributes(), output_fields)

    for attr in attrs:
        row = []
        row.append(attr)
        row.append(getattr(item, attr))
        x.add_row(row)
    return x


def print_list(parsed_args, item_generator, output_fields):
    if parsed_args.is_machine_readable:
        print_machine_readable_list(item_generator, output_fields)
    else:
        out = get_pretty_table(item_generator, output_fields)
        if out:
            print(out)


def print_machine_readable_list(items, output_fields):
    attrs = None
    for i in items:
        if attrs is None:
            attrs = _filter_attributes(i.get_attributes(), output_fields)
            print(",".join(attrs))
        row = []
        for attr in attrs:
            v = getattr(i, attr)
            row.append(v)
        print(",".join(map(str, row)))


def get_pretty_table(categories, output_fields):
    attrs = None
    x = None
    for c in categories:
        if attrs is None:
            attrs = _filter_attributes(c.get_attributes(), output_fields)
            x = PrettyTable(attrs)

        row = []
        for attr in attrs:
            row.append(getattr(c, attr))
        x.add_row(row)
    return x


def get_pretty_json(json_schema):
    return json_schema


def print_stats(parsed_args, stats):
    if parsed_args.is_machine_readable:
        print_machine_readable_stats(stats)
    else:
        out = get_print_pretty_table_stats(stats)
        print(out)


def print_machine_readable_stats(stats):
    # list is necessary, because keys are set-alike view
    keys = sorted(list(stats.keys()))
    print(",".join(keys))

    row = []
    for k in keys:
        row.append("{0}".format(stats[k]))
    print(",".join(row))


def get_print_pretty_table_stats(stats):
    # list is necessary, because keys are set-alike view
    keys = sorted(list(stats.keys()))
    x = PrettyTable(keys)

    row = []
    for k in keys:
        row.append("{0}".format(stats[k]))
    x.add_row(row)
    return x
