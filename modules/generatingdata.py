import json
import random
import math
from itertools import count
import itertools


def generate_random_data(weaponTypeCount, targetCount):
    targetWeights = [random.randint(10, 100) for _ in range(targetCount)]
    weaponsSupply = [random.randint(1, 3) for _ in range(weaponTypeCount)]
    position = [random.randint(1000, 1500) for _ in range(targetCount)] # m
    weaponRange = [random.randint(100, 1000) for _ in range(weaponTypeCount)]  # m

    probabilities = []
    for _ in range(weaponTypeCount):
        probabilities.append([round(random.uniform(0, 0.9), 3) for _ in range(targetCount)])

    data = {
        "weaponTypeCount": weaponTypeCount,
        "targetCount": targetCount,
        "targetWeights": targetWeights,
        "weaponsSupply": weaponsSupply,
        "propabilities": probabilities,
        "position": position,
        "weaponRange": weaponRange
    }

    # Zapisywanie danych do pliku JSON
    with open(f'../data/{weaponTypeCount}x{targetCount}.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print("Dane zostały wygenerowane i zapisane w pliku random_data.json.")

    return data


# Generowanie danych

# weaponTypeCount = 50
# targetCount = 50
# random_data = generate_random_data(weaponTypeCount, targetCount)
