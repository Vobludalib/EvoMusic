import miditoolkit
import generators

def generate_population(population_size, number_of_notes_mean, number_of_notes_std, pitch_range, duration_range, length):
    population = []
    for _ in range(population_size):
        individual = generators.generate_individual(number_of_notes_mean, number_of_notes_std, pitch_range, duration_range, length)
        population.append(individual)
    return population