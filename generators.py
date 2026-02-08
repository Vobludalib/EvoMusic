import miditoolkit
import numpy as np

def generate_individual(number_of_notes_mean, number_of_notes_std, pitch_range, duration_range, length):
    number_of_notes = max(1, int(np.random.normal(number_of_notes_mean, number_of_notes_std)))
    individual = []
    for _ in range(number_of_notes):
        pitch = np.random.randint(pitch_range[0], pitch_range[1])
        duration = np.random.randint(duration_range[0], duration_range[1])
        start = np.random.randint(0, length-duration)  # Random start time, can be adjusted as needed
        velocity = int(np.random.normal(64, 10))  # Random velocity, can be adjusted as needed
        individual.append(miditoolkit.Note(velocity, pitch, start, start+duration))
        individual.sort(key=lambda note: (note.start, note.duration))  # Sort notes by start time
    return individual
