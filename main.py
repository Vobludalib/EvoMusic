from miditoolkit.midi import parser as mid_parser
from miditoolkit.pianoroll import parser as pr_parser
from miditoolkit.pianoroll import utils
import tqdm
import evolution
import evaluators
import midi_io
import selectors
import crossovers
import mutators
import numpy as np
import matplotlib.pyplot as plt

path_midi = './Prelude1.mid'
mido_obj = mid_parser.MidiFile(path_midi)
notes = mido_obj.instruments[0].notes

min_note = 28
max_note = 108
pitch_range = (min_note, max_note)

ticks_per_beat = mido_obj.ticks_per_beat

target_pr = pr_parser.notes2pianoroll(
                    notes, pitch_range)[0:ticks_per_beat*4, :]  # Use only the first 4 beats for simplicity

population_size = 100
population = evolution.generate_population(population_size, 5, 2, (60, 80), (int(ticks_per_beat*0.25), int(ticks_per_beat*2)), ticks_per_beat*4)

min_fitnesses = []
mean_fitnesses = []
gens = []

minor_mut_rate = 0.05
major_mut_rate = 0.1

best_individual = None
best_fitness = float('inf')
for generation in range(100):
    fitnesses = []
    for i in range(len(population)):
        fitness = evaluators.evaluate_individual(population[i], target_pr, pitch_range = pitch_range)
        fitnesses.append(fitness)
        if fitness < best_fitness:
            best_fitness = fitness
            best_individual = population[i]

    print(f"Gen {generation}: {np.min(fitnesses)}, {np.mean(fitnesses)}")

    parents = selectors.select(population, fitnesses, num_parents=population_size//2)

    new_pop = []

    for parent_pair in zip(parents, parents[1:] + [parents[0]]):  # Pair each parent with the next one (circular)
        child1, child2 = crossovers.alternate_crossover(parent_pair[0], parent_pair[1])
        child1 = mutators.mutate(child1, add_note_rate=minor_mut_rate, remove_note_rate=minor_mut_rate, change_pitch_rate=major_mut_rate, change_duration_rate=major_mut_rate, change_start_rate=major_mut_rate, duration_range=(int(ticks_per_beat*0.25), int(ticks_per_beat*2)), length=ticks_per_beat*4)
        child2 = mutators.mutate(child2, add_note_rate=minor_mut_rate, remove_note_rate=minor_mut_rate, change_pitch_rate=major_mut_rate, change_duration_rate=major_mut_rate, change_start_rate=major_mut_rate, duration_range=(int(ticks_per_beat*0.25), int(ticks_per_beat*2)), length=ticks_per_beat*4)
        new_pop.append(child1)
        new_pop.append(child2)

    population = new_pop
    
    min_fitnesses.append(np.min(fitnesses))
    mean_fitnesses.append(np.mean(fitnesses))
    gens.append(generation)

midi_io.notes_to_midi(best_individual, 'output.mid', ticks_per_beat=ticks_per_beat)

# A straightforward min/max plot
plt.figure()
plt.plot(gens, mean_fitnesses, label='mean')
plt.plot(gens, min_fitnesses, label='min')
plt.xlabel('Generation')
plt.ylabel('Fitness (lower is better)')
plt.title('Min, Mean, and Max (running) Fitness over Generations')
plt.legend()
plt.tight_layout()
plt.savefig('min_max_fitness.png')
plt.show()


