from random import uniform

def arithmetic_co(p1, p2):
    
    #make a copy of the weights of the parents
    weights1, weights2 = p1.weights.copy(), p2.weights.copy()
    
    # Set a value for alpha between 0 and 1
    alpha = uniform(0,1)
    
    # Take weighted sum of two parents, invert alpha for second offspring
    # Perform each pair of computations in a single line so the result of the first computation does not affect the second computation
    for i in range(len(weights1)):
        weights1[i], weights2[i] = (weights1[i] * alpha + (1 - alpha) * weights2[i]), (weights2[i] * alpha + (1 - alpha) * weights1[i])

    if p1.verbose:
        print()
        print('Arithmetic crossover performed on individuals ' + str(p1.ind_number) + ' and ' + str(p2.ind_number) +'.')

    return weights1, weights2