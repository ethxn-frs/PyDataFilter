def filter_data(data, field, condition, value):
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
    elif condition == "greater_than":
        return [item for item in data if item.get(field) > value]
    elif condition == "greater_than_equals":
        return [item for item in data if item.get(field) >= value]
    elif condition == "true":
        return [item for item in data if item.get(field) is True]
    elif condition == "false":
        return [item for item in data if item.get(field) is False]
    return data
