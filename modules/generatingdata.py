import json
import random
import math
from itertools import count
import itertools


def generate_random_data(t, weaponTypeCount, targetCount):
    timeDim = t
    targetWeights = [random.randint(10000, 100000) for _ in range(targetCount)]
    weaponsSupply = [random.randint(1, 3) for _ in range(weaponTypeCount)]
    targetStartingPosition = [random.randint(1000, 1500) for _ in range(targetCount)]  # m
    targetVelocity = [random.randint(100, 120) for _ in range(targetCount)]  # m/s
    weaponRange = [random.randint(900, 2000) for _ in range(weaponTypeCount)]  # m

    probabilities = []
    for _ in range(weaponTypeCount):
        probabilities.append([round(random.uniform(0, 0.9), 3) for _ in range(targetCount)])

    data = {
        "timeDim": timeDim,
        "weaponTypeCount": weaponTypeCount,
        "targetCount": targetCount,
        "targetWeights": targetWeights,
        "weaponsSupply": weaponsSupply,
        "propabilities": probabilities,
        "targetStartingPosition": targetStartingPosition,
        "targetVelocity": targetVelocity,
        "weaponRange": weaponRange
    }

    return data


t = 50
weaponTypeCount = 50
targetCount = 50

# Generowanie danych
random_data = generate_random_data(t, weaponTypeCount, targetCount)

# Zapisywanie danych do pliku JSON
with open(f'../data/testInstance{t}x{weaponTypeCount}x{targetCount}.json', 'w') as json_file:
    json.dump(random_data, json_file, indent=2)

print("Dane zostały wygenerowane i zapisane w pliku random_data.json.")
