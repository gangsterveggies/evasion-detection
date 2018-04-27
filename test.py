from simulation import simulate
import random

def test(nm, n, m, base):
    res_model = simulate(n, m, base)
    res_uniform = simulate(n, m, base, c = [m / n for _ in range(n)])
    random_c = [random.random() for _ in range(n)]
    random_c = [m * i / sum(random_c) for i in range(n)]
    res_random = simulate(n, m, base, c = random_c)

    res_model = int(res_model)
    res_uniform = int(res_uniform)
    res_random = int(res_random)

    if nm != 1: print()
    print("----- Test " + str(nm) + " -----")
    print()
    print("Parameters:")
    print("\tn = " + str(n))
    print("\tm = " + str(m))
    print("\tbase = " + str(base))
    print()
    print("Results:")
    print("\tModel utility:   " + str(res_model))
    print("\tUniform utility: " + str(res_uniform))
    print("\tRandom utility:  " + str(res_random))

if __name__ == '__main__':
    test(1, 100, 5, 0.3)
    test(2, 500, 10, 0.2)
    test(3, 2000, 100, 0.15)
#    test(4, 10000, 200, 0.1)
