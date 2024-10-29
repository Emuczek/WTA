import json
import random


def generate_random_data(weaponTypeCount, targetCount):
    # Generowanie losowych wag celów
    targetWeights = [random.randint(1, 100) for _ in range(targetCount)]

    # Generowanie losowych zapasów broni
    weaponsSupply = [random.randint(1, 1) for _ in range(weaponTypeCount)]

    # Generowanie losowych prawdopodobieństw
    probabilities = []
    for _ in range(weaponTypeCount):
        probabilities.append([round(random.uniform(0, 0.9), 3) for _ in range(targetCount)])

    # Tworzenie struktury danych
    data = {
        "weaponTypeCount": weaponTypeCount,
        "targetCount": targetCount,
        "targetWeights": targetWeights,
        "weaponsSupply": weaponsSupply,
        "propabilities": probabilities
    }

    return data


# Ustawienia
weaponTypeCount = 50  # Zmienna do określenia liczby typów broni
targetCount = 50  # Zmienna do określenia liczby celów

# Generowanie danych
random_data = generate_random_data(weaponTypeCount, targetCount)

# Zapisywanie danych do pliku JSON
with open('../data/random_data.json', 'w') as json_file:
    json.dump(random_data, json_file, indent=2)

print("Dane zostały wygenerowane i zapisane w pliku random_data.json.")
