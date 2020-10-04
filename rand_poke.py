import pandas as pd
import random
import numpy as np
import random

def random_pokemon(type1, type2 = None):
    df = pd.read_csv("pokemon.csv", encoding="UTF-8")
    df = df.replace(np.nan, "None")
    if type2 is None: 
        type2 = random.choice(df["Type 2"].unique())
    
    possibilities = df[(df["Type 1"] == type1) & (df["Type 2"] == type2)]
    
    poke_list = possibilities["Name"].tolist()
    
    if len(poke_list) is not 0: random_poke = random.choice(poke_list)
    else: random_poke = None
    
    return random_poke
