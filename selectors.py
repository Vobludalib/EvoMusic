import random

def roulette_select(population, fitnesses, num_parents):
    """Roulette-wheel selection where lower fitness is preferred.

    Converts fitness values to selection weights by inverting them (1 / (fitness + eps)).
    Samples `num_parents` individuals with probability proportional to these weights.
    """
    eps = 1e-8
    # Ensure we have a list copy
    fits = list(fitnesses)

    # If all fitnesses are identical (or zeros), fall back to uniform selection
    if all(abs(f - fits[0]) < eps for f in fits):
        return random.choices(population, k=num_parents)

    # Invert fitness so that lower fitness => higher weight
    inv_weights = [1.0 / (f + eps) for f in fits]
    total = sum(inv_weights)
    if total <= 0:
        # defensive: uniform selection
        return random.choices(population, k=num_parents)

    # Normalize weights and perform roulette sampling (with replacement)
    weights = [w / total for w in inv_weights]
    return random.choices(population, weights=weights, k=num_parents)

def linear_rank_select(population, fitnesses, num_parents):
    """Linear rank selection where lower fitness is preferred.

    Ranks individuals by fitness and assigns selection probabilities based on rank.
    """
    # Sort population by fitness (lower is better)
    sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1])
    ranked_population = [ind for ind, fit in sorted_population]

    # Assign selection probabilities based on rank
    n = len(population)
    total_rank = n * (n + 1) / 2  # Sum of ranks from 1 to n
    probabilities = [(n - rank) / total_rank for rank in range(n)]  # Higher rank => higher probability

    # Sample parents based on these probabilities
    return random.choices(ranked_population, weights=probabilities, k=num_parents)