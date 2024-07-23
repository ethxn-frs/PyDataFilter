def filter_data(data, field, condition, value):
    def safe_get(item, key, default=''):
        return item.get(key, default)

    if condition == "equals":
        return [item for item in data if item.get(field) == value]
    elif condition == "not_equals":
        return [item for item in data if item.get(field) != value]
    elif condition == "contains":
        return [item for item in data if value in item.get(field, '')]
    elif condition == "not_contains":
        return [item for item in data if value not in item.get(field, '')]
    elif condition == "less_than":
        return [item for item in data if item.get(field) < value]
    elif condition == "less_than_equals":
        return [item for item in data if item.get(field) <= value]
    elif condition == "lexicographically_less_than":
        return [item for item in data if item.get(field, '').lower() < value.lower()]
    elif condition == "lexicographically_greater_than":
        return [item for item in data if item.get(field, '').lower() > value.lower()]
    elif condition == "starts_with":
        return [item for item in data if item.get(field, '').lower().startswith(value)]
    elif condition == "ends_with":
        return [item for item in data if item.get(field, '').lower().endswith(value)]
    elif condition == "greater_than":
        return [item for item in data if item.get(field) > value]
    elif condition == "greater_than_equals":
        return [item for item in data if item.get(field) >= value]
    elif condition == "lexicographically_less_than_field":
        return [item for item in data if safe_get(item, field, '').lower() < safe_get(item, value, '').lower()]
    elif condition == "lexicographically_greater_than_field":
        return [item for item in data if safe_get(item, field, '').lower() > safe_get(item, value, '').lower()]
    elif condition == "true":
        return [item for item in data if item.get(field) is True]
    elif condition == "false":
        return [item for item in data if item.get(field) is False]
    elif condition == "exact_length":
        return [item for item in data if len(item.get(field, [])) == int(value)]
    elif condition == "min_length":
        return [item for item in data if len(item.get(field, [])) >= int(value)]
    elif condition == "max_length":
        return [item for item in data if len(item.get(field, [])) <= int(value)]
    elif condition == "average_equals":
        return [item for item in data if (sum(item.get(field, [])) / len(item.get(field, []))) == float(value)]
    elif condition == "average_less":
        return [item for item in data if (sum(item.get(field, [])) / len(item.get(field, []))) < float(value)]
    elif condition == "average_greater":
        return [item for item in data if (sum(item.get(field, [])) / len(item.get(field, []))) > float(value)]
    return data
