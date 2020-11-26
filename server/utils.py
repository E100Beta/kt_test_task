import datetime


def prepare_records(records):

    def line_to_dict(record):
        line = {}
        for key, value in record.items():
            # json.loads doesn't like datetime
            if isinstance(value, datetime.datetime):
                line[key] = value.isoformat()
            else:
                line[key] = value
        return line

    # if single record
    if hasattr(records, 'keys'):
        return line_to_dict(records)
    result = []
    for record in records:
        line = line_to_dict(record)
        result.append(line)
    return result
