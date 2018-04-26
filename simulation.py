import data, model, random
import numpy as np

def gen_population(n, distribution):
    population = []

    for element in distribution:
        to_add = int(2 + n * element[1] / 100.0)
        for _ in range(to_add):
            population.append(random.randint(element[0][0], element[0][1]))

    random.shuffle(population)
    population = population[:n]
    population.sort()

    return population

def draw_from_c(c, m):
    tot = sum(c)
    normalized_c = [i / tot for i in c]
    return np.random.choice(len(c), size = m, replace = False, p = normalized_c)

def search_income(value, a):
    for i in range(len(a)):
        if value >= a[i][0][0] and value <= a[i][0][1]:
            return a[i][1]
    return None

def gen_threshold(n, m, population, distribution):
    return [random.random() * (0.5 * (1 + search_income(population[i], distribution) / 100)) for i in range(n)]

def draw_from_threshold(c, threshold):
    evaders = []

    for i in range(len(c)):
        if random.random() <= threshold[i] - c[i]:
            evaders.append(i)

    return evaders

def deterministic_defender_utility(audits, evaders, population):
    ud = lambda t: data.kv * population[t]
    return sum([ud(t) for t in evaders if t in audits]) - sum([data.ka * population[t] for t in audits])

def simulate(n, m, c = None, verbose = False):
    population = gen_population(n, data.income_distribution)
    threshold = gen_threshold(n, m, population, data.audits_distribution)

    if c == None:
        if verbose: print("Generating model...")
        c = model.gen_model(population, m, verbose = True)
        print(c)

    if verbose:
        evaders = draw_from_threshold(c, threshold)
        print(threshold)
        print(evaders)

    avg_u = 0
    for _ in range(data.simulation_iteration_number):
        audits = draw_from_c(c, m)
        evaders = draw_from_threshold(c, threshold)
        avg_u += deterministic_defender_utility(audits, evaders, population)
    avg_u /= data.simulation_iteration_number

    return avg_u

if __name__ == '__main__':
    n, m = (40, 5)

    res_model = simulate(n, m, verbose = True)
    res_uniform = simulate(n, m, c = [m / n for _ in range(n)])

    print("Model utility: " + str(res_model))
    print("Uniform utility: " + str(res_uniform))
