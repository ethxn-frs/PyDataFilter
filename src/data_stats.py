def calculate_statistics(data):
    stats = {}
    for key in data[0].keys():
        values = [item[key] for item in data]
        if all(isinstance(v, (int, float)) for v in values):
            stats[key] = {
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values)
            }
        elif all(isinstance(v, bool) for v in values):
            stats[key] = {
                'true': sum(values) / len(values) * 100,
                'false': (len(values) - sum(values)) / len(values) * 100
            }
        elif all(isinstance(v, list) for v in values):
            list_lengths = [len(v) for v in values]
            stats[key] = {
                'min': min(list_lengths),
                'max': max(list_lengths),
                'avg': sum(list_lengths) / len(list_lengths)
            }
    return stats