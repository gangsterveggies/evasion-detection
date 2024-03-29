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

def gen_threshold(n, m, population, distribution, base):
    return [random.random() * (base * (1 + search_income(population[i], distribution) / 100)) for i in range(n)]

def draw_from_threshold(c, threshold, population):
    evaders = []

    for i in range(len(c)):
        if model.attacker_utility(c, i, population) >= 0 and random.random() <= threshold[i]:
            evaders.append(i)

    return evaders

def draw_from_threshold2(threshold):
    evaders = []

    for i in range(len(threshold)):
        if random.random() <= threshold[i]:
            evaders.append(i)

    return evaders

def deterministic_defender_utility(audits, evaders, population):
    ud = lambda t: data.kv * population[t]
    return sum([ud(t) for t in evaders if t in audits]) - sum([data.ka * population[t] for t in audits])

def simulate(n, m, base, c = None, verbose = False):
    population = gen_population(n, data.income_distribution)
    threshold = gen_threshold(n, m, population, data.audits_distribution, base)

    if c == None:
        if verbose: print("Generating model...")
        c = model.gen_model(population, m, verbose = verbose)

    avg_u = 0
    avg_evaders = 0
    for _ in range(data.simulation_iteration_number):
        audits = draw_from_c(c, m)
        evaders = draw_from_threshold(c, threshold, population)
        avg_evaders += len(evaders)
        avg_u += deterministic_defender_utility(audits, evaders, population)
    avg_u /= data.simulation_iteration_number
    avg_evaders /= data.simulation_iteration_number

    if verbose: print("Average number of evaders: " + str(avg_evaders))

    return avg_u

if __name__ == '__main__':
    n, m = (1000, 20)

    res_model = simulate(n, m, 0.3, verbose = True)
    res_uniform = simulate(n, m, 0.3, c = [m / n for _ in range(n)])

    print("Model utility: " + str(res_model))
    print("Uniform utility: " + str(res_uniform))
