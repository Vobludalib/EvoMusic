import miditoolkit
import numpy as np

def alternate_crossover(parent1, parent2):
    offspring1 = []
    offspring2 = []
    for i in range(max(len(parent1), len(parent2))):
        if i % 2 == 0:
            if i < len(parent1):
                offspring1.append(parent1[i])
            if i < len(parent2):
                offspring2.append(parent2[i])
        else:
            if i < len(parent2):
                offspring1.append(parent2[i])
            if i < len(parent1):
                offspring2.append(parent1[i])

    

    return offspring1, offspring2