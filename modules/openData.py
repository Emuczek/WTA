import json
import numpy as np
import pandas as pd

# 'C:/Users/Jakub/PycharmProjects/pythonProject/data/testInstance2x2.json'


def explosionprequel(n: int):
    if n > 1:
        return np.ones(n)
    else:
        return n


def opendata(data_path: str, binarize: bool):
    with open(data_path) as json_file:
        data = json.load(json_file)

        if binarize:
            m = data['weaponTypeCount']  # number of weapons
            n = data['targetCount']  # number of incoming targets
            v = data['targetWeights']  # number describing target importance
            data.pop('weaponTypeCount')
            data.pop('targetCount')
            data.pop('targetWeights')
            df = pd.DataFrame.from_dict(data)
            df['weaponsSupply'] = df['weaponsSupply'].apply(explosionPrequel)
            df = df.explode('weaponsSupply')
            p = df['propabilities'].tolist()
            return len(p), len(p[0]), v, df['weaponsSupply'].astype(int).tolist(), p
        else:
            m = data['weaponTypeCount']  # number of weapons
            n = data['targetCount']  # number of incoming targets
            v = data['targetWeights']  # number describing target importance
            w = data['weaponsSupply']  # number of each weapon by weapon type
            p = data['propabilities']  # propability of weapon type m of destroying target n
        return m, n, v, w, p


# print(openData('C:/Users/Jakub/PycharmProjects/pythonProject/data/testInstance2x2.json', True))