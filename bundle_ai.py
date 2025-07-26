import random
import pandas as pd

# GA Configuration
MUTATION_RATE = 0.2
POPULATION_SIZE = 10
GENERATIONS = 100
FITNESS_THRESHOLD = 1.0
ELITISM_COUNT = 1

def load_dataset(filepath):
    df = pd.read_csv(filepath)
    return [tuple(row) for row in df.to_numpy()]

def fitness(bundle, cost_limit, weight_limit):
    total_cost = sum(item[1] for item in bundle)
    total_selling_price = sum(item[2] for item in bundle)
    total_weight = sum(item[3] for item in bundle)
    total_value = sum(item[4] for item in bundle)

    penalty = 0
    reward = 0

    if total_cost > cost_limit:
        penalty += 1
    if total_weight > weight_limit:
        penalty += 1

    if total_value >= 60:
        reward = 1.0
    elif total_value >= 30:
        reward = 0.5

    return (total_selling_price / cost_limit) - penalty + reward

def initialize_population(products):
    return [random.sample(products, random.randint(2, len(products)//2)) for _ in range(POPULATION_SIZE)]

def selection(population, products, cost_limit, weight_limit):
    scores = [fitness(b, cost_limit, weight_limit) for b in population]
    total_score = sum(scores)
    if total_score == 0:
        return random.sample(population, 2)
    probs = [s / total_score for s in scores]
    return random.choices(population, weights=probs, k=2)

def crossover(parent1, parent2):
    if len(parent1) < 2 or len(parent2) < 2:
        return parent1 if random.random() > 0.5 else parent2
    cut = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child = parent1[:cut] + parent2[cut:]
    return list(set(child))

def mutate(bundle, products):
    if random.random() < MUTATION_RATE and bundle:
        index = random.randint(0, len(bundle) - 1)
        bundle[index] = random.choice(products)
    return bundle

def run_bundle_ai(filepath, cost_limit, weight_limit, repeat_runs=10):
    random.seed(42)
    products = load_dataset(filepath)
    best_bundle = None
    best_score = -float('inf')

    for _ in range(repeat_runs):
        population = initialize_population(products)
        for _ in range(GENERATIONS):
            elites = sorted(population, key=lambda b: fitness(b, cost_limit, weight_limit), reverse=True)[:ELITISM_COUNT]
            new_pop = elites[:]
            while len(new_pop) < POPULATION_SIZE:
                p1, p2 = selection(population, products, cost_limit, weight_limit)
                c1 = crossover(p1, p2)
                c2 = crossover(p2, p1)
                new_pop.extend([mutate(c1, products), mutate(c2, products)])
            population = sorted(new_pop, key=lambda b: fitness(b, cost_limit, weight_limit), reverse=True)[:POPULATION_SIZE]

        current = population[0]
        score = fitness(current, cost_limit, weight_limit)
        if score > best_score:
            best_score = score
            best_bundle = current

    # Prepare result
    result = {
        "bundle_size": len(best_bundle),
        "total_cost": round(sum(item[1] for item in best_bundle), 2),
        "total_weight": round(sum(item[3] for item in best_bundle), 2),
        "total_value": sum(item[4] for item in best_bundle),
        "fitness_score": round(best_score, 3),
        "products": [item[0] for item in best_bundle]
    }
    return result
