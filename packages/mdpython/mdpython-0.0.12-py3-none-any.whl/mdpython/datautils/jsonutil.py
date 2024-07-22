import csv


def flatten_json(json_data, parent_key='', separator='.'):
    items = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, separator=separator))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.update(flatten_json(item, f"{new_key}{separator}{i}",
                                              separator=separator))
                elif isinstance(item, list):
                    items.update(flatten_json({"sublist": item},
                                              f"{new_key}{separator}{i}",
                                              separator=separator))
                else:
                    items[f"{new_key}{separator}{i}"] = item
        else:
            items[new_key] = value
    return items


def list_to_csv(data_list_inp, file_name, colkey=None):
    if colkey is None:
        colkey = []
    data_list = [flatten_json(x) for x in data_list_inp]
    if not colkey:
        all_keys = sorted(set().union(*(d.keys() for d in data_list)))
    else:
        all_keys = colkey

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        for item in data_list:
            row = {key: item.get(key, '') for key in all_keys}
            writer.writerow(row)
