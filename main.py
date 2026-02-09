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
import visualiser
import matplotlib.pyplot as plt
import time

path_midi = './Prelude1.mid'
mido_obj = mid_parser.MidiFile(path_midi)
notes = mido_obj.instruments[0].notes

ticks_per_beat = mido_obj.ticks_per_beat
min_note = 28
max_note = 108
pitch_range = (min_note, max_note)
duration_range = (0, ticks_per_beat*4)  # Up to 4 beats in duration

target_pr = pr_parser.notes2pianoroll(
                    notes, pitch_range)[0:ticks_per_beat*4, :]  # Use only the first 4 beats for simplicity

population_size = 100
population = evolution.generate_population(population_size, 12, 2, (60, 80), (int(ticks_per_beat*0.25), int(ticks_per_beat*2)), ticks_per_beat*4)

min_fitnesses = []
mean_fitnesses = []
gens = []

minor_mut_rate = 0.2
major_mut_rate = 0.1
starting_regen_rate = 0.3
ending_regen_rate = 0.02

best_individual = None
best_fitness = float('inf')
generations = 100
for generation in range(generations):
    print(f"Generation {generation}")
    fitnesses = []
    best_gen_fitness = float('inf')
    best_gen_individual = None
    eval_time = 0
    for i in range(len(population)):
        start = time.perf_counter()
        fitness = evaluators.evaluate_individual(population[i], target_pr, pitch_range = pitch_range)
        eval_time += time.perf_counter() - start
        fitnesses.append(fitness)
        if fitness < best_fitness:
            best_fitness = fitness
            best_individual = population[i]
        if fitness < best_gen_fitness:
            best_gen_fitness = fitness
            best_gen_individual = population[i]

    print(f"Evaluation time for generation {generation}: {eval_time:.2f} seconds")

    percent_regen = starting_regen_rate + (ending_regen_rate - starting_regen_rate) * (generation / generations)
    parents = selectors.linear_rank_select(population, fitnesses, num_parents=int(2*(population_size*(1-percent_regen))))
    amount_to_generate = population_size - len(parents)

    new_pop = []

    crossover_time = 0
    mutate_time = 0
    for parent_pair in zip(parents, parents[1:] + [parents[0]]):  # Pair each parent with the next one (circular)
        start = time.perf_counter()
        child1, child2 = crossovers.alternate_crossover(parent_pair[0], parent_pair[1])
        crossover_time += time.perf_counter() - start
        start = time.perf_counter()
        child1 = mutators.mutate(child1, add_note_rate=minor_mut_rate/2, remove_note_rate=minor_mut_rate, split_note_rate=major_mut_rate/2, change_pitch_rate=major_mut_rate, change_duration_rate=major_mut_rate, change_start_rate=major_mut_rate, duration_range=(int(ticks_per_beat*0.25), int(ticks_per_beat*2)), length=ticks_per_beat*4)
        child2 = mutators.mutate(child2, add_note_rate=minor_mut_rate/2, remove_note_rate=minor_mut_rate, split_note_rate=major_mut_rate/2, change_pitch_rate=major_mut_rate, change_duration_rate=major_mut_rate, change_start_rate=major_mut_rate, duration_range=(int(ticks_per_beat*0.25), int(ticks_per_beat*2)), length=ticks_per_beat*4)
        mutate_time += time.perf_counter() - start
        new_pop.append(child1)
        new_pop.append(child2)

    print(f"Crossover time for generation {generation}: {crossover_time:.2f} seconds")
    print(f"Mutation time for generation {generation}: {mutate_time:.2f} seconds")

    population = new_pop
    generated_pop = evolution.generate_population(amount_to_generate, 12, 2, (60, 80), (int(ticks_per_beat*0.25), int(ticks_per_beat*2)), ticks_per_beat*4)
    population.extend(generated_pop)
    
    min_fitnesses.append(np.min(fitnesses))
    mean_fitnesses.append(np.mean(fitnesses))
    gens.append(generation)

    # Visualise the best individual every 10 generations
    # if generation % 10 == 0:
    visualiser.plot_piano_roll(pr_parser.notes2pianoroll(best_gen_individual, pitch_range, time_portion=duration_range), target_pr, f'img\\output.png')

    print(f"Gen {generation}: {np.min(fitnesses)}, {np.mean(fitnesses)}")

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


