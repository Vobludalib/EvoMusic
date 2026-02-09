import miditoolkit
import numpy as np
from miditoolkit.pianoroll import parser as pr_parser
from miditoolkit.pianoroll import utils

def evaluate_individual(individual, target_pr, pitch_range):
    ind_pr = pr_parser.notes2pianoroll(individual, pitch_range)
    
    # Pad ind_pr to match target_pr shape
    pad_time = max(0, target_pr.shape[0] - ind_pr.shape[0])
    pad_pitch = max(0, target_pr.shape[1] - ind_pr.shape[1])
    ind_pr = np.pad(ind_pr, ((0, pad_time), (0, pad_pitch)), mode='constant', constant_values=0)

    # Calculate fitness as the sum of squared differences between the two pianorolls
    fitness = 0
    for i in range(target_pr.shape[0]):
        for j in range(target_pr.shape[1]):
            if target_pr[i, j] > 0 and ind_pr[i, j] == 0:
                fitness += 100 # Penalize missing notes heavily
            else:
                fitness += (int((target_pr[i, j] - ind_pr[i, j])) ** 2) / 100 # Penalize differences in velocity
            # fitness += 1 if target_pr[i, j] != ind_pr[i, j] else 0

    return fitness