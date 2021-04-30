from random import uniform

def arithmetic_co(p1, p2):
    
    # Set a value for alpha between 0 and 1
    alpha = uniform(0,1)

    # Take weighted sum of two parents, invert alpha for second offspring
    # Perform each pair of computations in a single line so the result of the first computation does not affect the second computation
    for i in range(len(p1)):
        p1[i], p2[i] = (p1[i] * alpha + (1 - alpha) * p2[i]), (p2[i] * alpha + (1 - alpha) * p1[i])

    if p1.verbose:
        print()
        print('Arithmetic crossover performed on individuals ' + str(p1.ind_number) + ' and ' + str(p2.ind_number) +'.')

    return p1, p2