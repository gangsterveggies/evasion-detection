from cvxpy import *
import random, data

def defender_utility_exact(c, attacker_list, population):
    n = len(population)
    ud = lambda c, t: data.kv * population[t] * c[t]
    return sum([ud(c, t) for t in attacker_list] + [-data.ka * population[t] * c[t] for t in range(n)])

def defender_utility_approximated(c, attacker_list, population):
    n = len(population)
    sampled = random.sample(range(n), min(n, 20))
    scale = n / len(sampled)
    ud = lambda c, t: data.kv * population[t] * c[t]
    return sum([ud(c, t) for t in attacker_list] + [-scale * data.ka * population[t] * c[t] for t in sampled])

def attacker_utility(c, attacker, population):
    n = len(population)
    uap = lambda t: -data.kv * population[t]
    uam = lambda t: data.ke * population[t]
    return uap(attacker) * c[attacker] + uam(attacker) * (1 - c[attacker])

def solve_LP(n, m, attacker_list, population):
    c = Variable(n)
    objective = Maximize(defender_utility_exact(c, attacker_list, population))
    constraints = [sum(c) == m, c <= 1, c >= 0] + [attacker_utility(c, attacker, population) >= 0 for attacker in attacker_list]

    prob = Problem(objective, constraints)
    result = prob.solve()

    if prob.status == OPTIMAL: return (result, True, c.value)
    else: return (result, False, [])

def gen_model(population, m, verbose = False):
    n = len(population)
    attacker_list = []

    for it in range(data.model_iteration_number):
        if (it + 1) % 10 == 0 and verbose: print("Model iteration " + str(it + 1))

        pt, vt, ct = solve_LP(n, m, attacker_list, population)
        c = [max(0, min(float(i), 1)) for i in ct]

        for t in range(n):
            if t in attacker_list:
                if attacker_utility(c, t, population) <= 0:
                    attacker_list.remove(t)
            else:
                if attacker_utility(c, t, population) >= 0:
                    attacker_list.append(t)

    pt, vt, ct = solve_LP(n, m, attacker_list, population)
    best_c = [max(0, min(float(i), 1)) for i in ct]
    best_utility = pt

    if verbose:
        print(len(attacker_list))

    return best_c

if __name__ =='__main__':
    population = [5000, 15000, 30000, 40000, 45000, 45000, 60000, 70000, 100000]
    m = 2

    c = gen_model(population, m, verbose = True)
    print(c)
