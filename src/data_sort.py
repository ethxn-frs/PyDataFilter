def sort_data(data, field, order):
    reverse = order == "descending" or order == "true_to_false" or order == "z_to_a"
    return sorted(data, key=lambda x: x[field], reverse=reverse)
