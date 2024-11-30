import json
import numpy as np
import pandas as pd


def explosionprequel(n: int):
    if n > 1:
        return np.ones(n)
    else:
        return n


def opendata(data_path: str, binarize: bool):
    with open(data_path) as json_file:
        data = json.load(json_file)
        # m, n, V, w, s, v, r, p
        if binarize:
            t = data['timeDim']
            m = data['weaponTypeCount']  # number of weapons
            n = data['targetCount']  # number of incoming targets
            V = data['targetWeights']  # number describing target importance
            s = data['targetStartingPosition']  # starting positions of targets
            v = data['targetVelocity']  # targets velocity
            r = data['weaponRange']  # ranges of weapons
            data.pop('timeDim')
            data.pop('weaponTypeCount')
            data.pop('targetCount')
            data.pop('targetWeights')
            data.pop('targetStartingPosition')
            data.pop('targetVelocity')
            data.pop('weaponRange')
            df = pd.DataFrame.from_dict(data)
            df['weaponsSupply'] = df['weaponsSupply'].apply(explosionprequel)
            df = df.explode('weaponsSupply')
            p = df['propabilities'].tolist()
            return t, len(p), len(p[0]), V, df['weaponsSupply'].astype(int).tolist(), p, s, v, r
        else:
            t = data['timeDim']
            m = data['weaponTypeCount']  # number of weapons
            n = data['targetCount']  # number of incoming targets
            V = data['targetWeights']  # number describing target importance
            w = data['weaponsSupply']  # number of each weapon by weapon type
            p = data['propabilities']  # propability of weapon type m of destroying target n
            s = data['targetStartingPosition']  # starting positions of targets
            v = data['targetVelocity']  # targets velocity
            r = data['weaponRange']  # ranges of weapons
        return t, m, n, V, w, p, s, v, r
