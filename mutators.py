import random
import miditoolkit
import numpy as np

def mutate(individual, add_note_rate, remove_note_rate, split_note_rate, change_pitch_rate, change_duration_rate, change_start_rate, duration_range, length):
    new_individual = []

    for note in individual:
        new_pitch = note.pitch
        new_duration = note.duration
        new_start = note.start
        if random.random() < change_pitch_rate:
            new_pitch = note.pitch + random.randint(-2, 2)  # Change pitch by a small random amount
            new_pitch = max(21, min(108, new_pitch))  # Ensure pitch stays within MIDI range

        if random.random() < change_duration_rate:
            new_duration = note.duration + random.randint(-10, 10)  # Change duration by a small random amount
            new_duration = max(1, new_duration)  # Ensure duration is positive

        if random.random() < change_start_rate:
            new_start = note.start + random.randint(-10, 10)  # Change start time by a small random amount
            new_start = max(0, new_start)  # Ensure start time is non-negative

        new_individual.append(miditoolkit.Note(note.velocity, new_pitch, new_start, new_start + new_duration))

    if random.random() < add_note_rate:
        duration = np.random.randint(duration_range[0], duration_range[1])
        start=np.random.randint(0, length-duration)
        new_note = miditoolkit.Note(
            velocity=int(np.random.normal(64, 10)),
            pitch=random.randint(60, 80),
            start=start, # Random start time, can be adjusted as needed
            end=start+duration
        )
        new_individual.append(new_note)
        
    if random.random() < remove_note_rate and len(new_individual) > 1:
        new_individual.pop(random.randint(0, len(new_individual) - 1))

    if random.random() < split_note_rate and len(new_individual) > 0:
        note_to_split = random.choice(new_individual)
        new_individual.remove(note_to_split)
        split_point = note_to_split.start + note_to_split.duration // 2
        first_half = miditoolkit.Note(note_to_split.velocity, note_to_split.pitch, note_to_split.start, split_point - note_to_split.duration // 5)
        second_half = miditoolkit.Note(note_to_split.velocity, note_to_split.pitch, split_point + note_to_split.duration // 5, note_to_split.end)
        new_individual.extend([first_half, second_half])
    
    new_individual.sort(key=lambda x: (x.start, x.duration))  # Ensure notes are sorted by start time

    return new_individual