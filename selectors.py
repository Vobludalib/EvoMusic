import random

def select(population, fitnesses, num_parents):
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