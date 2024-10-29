import json
import random


def generate_random_data(weaponTypeCount, targetCount):
    targetWeights = [random.randint(1, 1000) for _ in range(targetCount)]
    weaponsSupply = [random.randint(1, 3) for _ in range(weaponTypeCount)]

    probabilities = []
    for _ in range(weaponTypeCount):
        probabilities.append([round(random.uniform(0, 0.9), 3) for _ in range(targetCount)])

    data = {
        "weaponTypeCount": weaponTypeCount,
        "targetCount": targetCount,
        "targetWeights": targetWeights,
        "weaponsSupply": weaponsSupply,
        "propabilities": probabilities
    }

    return data


weaponTypeCount = input()
targetCount = input()

# Generowanie danych
random_data = generate_random_data(weaponTypeCount, targetCount)

# Zapisywanie danych do pliku JSON
with open('../data/testInstance50x50.json', 'w') as json_file:
    json.dump(random_data, json_file, indent=2)

print("Dane zostały wygenerowane i zapisane w pliku random_data.json.")
