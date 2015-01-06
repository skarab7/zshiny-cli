from prettytable import PrettyTable


def get_print_for_item(item, output_fields):

    attrs = _filter_attributes(item.get_attributes(), output_fields)

    for attr in attrs:
        row = []
        row.append(attr)
        row.append(str(getattr(item, attr)))
        print(",".join(row))
    return ""


def _filter_attributes(attrs, output_fields):
    return [attr for attr in attrs
            if should_attr_be_printed(output_fields, attr)]


def should_attr_be_printed(output_fields, attr):
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


def get_pretty_table(categories, output_fields):
    attrs = None
    for c in categories:
        if attrs is None:
            attrs = _filter_attributes(c.get_attributes(), output_fields)
            x = PrettyTable(attrs)

        row = []
        for attr in attrs:
            row.append(getattr(c, attr))
        print(row)
        x.add_row(row)
    else:
        x = ""
    return x


def get_pretty_json(json_schema):
    return json_schema
