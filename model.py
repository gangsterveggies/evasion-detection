from cvxpy import *
import random, data

def perturb(n, attacker_list):
    perturbed_list = list(attacker_list)

    # Remove half randomly
    random.shuffle(perturbed_list)
    perturbed_list = perturbed_list[0:len(perturbed_list) // 2]

    # Add more elements randomly
    to_add = min(len(perturbed_list), 10)
    perturbed_set = set(perturbed_list)
    for i in range(to_add):
        element = random.choice()
        if not(element in perturbed_set):
            perturbed_list.append(element)
            perturbed_set.add(element)

    return perturbed_list

def defender_utility(c, attacker_list, population):
    n = len(population)
    ud = lambda c, t: data.kv * population[t] * c[t]
    return sum([ud(c, t) for t in attacker_list]) - sum([data.ka * population[t] * c[t] for t in range(n)])

def attacker_utility(c, attacker, population):
    n = len(population)
    uap = lambda t: -data.kv * population[t]
    uam = lambda t: data.ke * population[t]
    return uap(attacker) * c[attacker] + uam(attacker) * (1 - c[attacker])

def solve_LP(n, m, attacker, attacker_list, population):
    c = Variable(n)
    objective = Maximize(defender_utility(c, attacker_list, population))
    #    constraints = [attacker_utility(c, attacker, attacker_list, population) >= attacker_utility(c, attacker, perturb(attacker_list), population) for _ in range(data.perturb_number)] + [sum(c) == m, c <= 1, c >= 0]

    constraints = [sum(c) == m, c <= 1, c >= 0] + [attacker_utility(c, attacker, population) >= 0]
        

    prob = Problem(objective, constraints)
    result = prob.solve()

    if prob.status == OPTIMAL: return (result, True, c.value)
    else: return (result, False, [])

def gen_model(population, m, verbose = False):
    n = len(population)
    best_c = [0 for i in range(n)]
    best_utility = -100000
    attacker_list = []

    for it in range(data.model_iteration_number):
        if verbose: print("Model iteration " + str(it + 1))
        population_order = [i for i in range(n)]
        random.shuffle(population_order)

        print_number = 1
        for t in population_order:
            if print_number % 10 == 0 and verbose: print("10 more individuals (" + str(n - print_number) + " remaining)")
            print_number += 1

            if t in attacker_list: attacker_list.remove(t)
            attacker_list.append(t)
            pt, vt, ct = solve_LP(n, m, t, attacker_list, population)

            if vt and pt > best_utility:
                best_c = ct
                best_utility = pt

            if vt:
                if attacker_utility([max(0, min(float(i), 1)) for i in best_c], t, population) <= 0:
                    attacker_list.pop()

    if verbose:
        print(len(attacker_list))
        print(best_utility)
    return [max(0, min(float(i), 1)) for i in best_c]

if __name__ =='__main__':
    population = [5000, 15000, 30000, 40000, 45000, 45000, 60000, 70000, 100000]
    m = 2

    c = gen_model(population, m)
    print(c)
