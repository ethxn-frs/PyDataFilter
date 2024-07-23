import ast


def calculate_statistics(data):
    stats = {}
    for key in data[0].keys():
        values = [item[key] for item in data if key in item]

        # Convertir les chaînes "true"/"false" en booléens
        for i in range(len(values)):
            if isinstance(values[i], str):
                if values[i].lower() == "true":
                    values[i] = True
                elif values[i].lower() == "false":
                    values[i] = False
                # Convertir les listes sous forme de chaînes en listes réelles
                elif values[i].startswith("[") and values[i].endswith("]"):
                    values[i] = ast.literal_eval(values[i])

        # Vérification robuste des types
        if all(isinstance(v, bool) for v in values):
            true_count = sum(values)
            false_count = len(values) - true_count
            stats[key] = {
                'true_percentage': true_count / len(values) * 100,
                'false_percentage': false_count / len(values) * 100
            }

        elif all(isinstance(v, (int, float)) for v in values):
            stats[key] = {
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values)
            }
        elif all(isinstance(v, list) for v in values):
            # Extraire les éléments des listes et combiner toutes les valeurs
            combined_values = [elem for sublist in values for elem in sublist]
            stats[key] = {
                'min': min(combined_values),
                'max': max(combined_values),
                'avg': sum(combined_values) / len(combined_values)
            }
        else:
            stats[key] = {'note': 'Type non pris en charge ou mixte'}
    return stats
