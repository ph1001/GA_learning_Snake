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

def uniform_co(p1, p2):
    
    #make a copy of the weights of the parents
    weights1, weights2 = p1.weights.copy(), p2.weights.copy()
    
    #We iterate over the weights (matrix, array, matrix, array) 
    for index in range(len(weights1)):
        
        if len(weights1[index].shape) > 1: #check if we are handling a matrix
            for i in range(weights1[index].shape[0]): #we iterate over the matrix
                for j in range(weights1[index].shape[1]):
                    if uniform(0, 1) > 0.5:#doing this 50% of the times
                        weights1[index][i,j] = p1.weights[index][i,j].copy()
                        weights2[index][i,j] = p2.weights[index][i,j].copy()
                    else:#otherwise the opposite
                        weights1[index][i,j] = p2.weights[index][i,j].copy()
                        weights2[index][i,j] = p1.weights[index][i,j].copy()
            
        else: #otherwise we are handling an array
            for j in range(len(weights1[index])): #iterate over array
                if uniform(0, 1) > 0.5:
                    weights1[index][j] = p1.weights[index][j].copy()
                    weights2[index][j] = p2.weights[index][j].copy()
                else:
                    weights1[index][j] = p2.weights[index][j].copy()
                    weights2[index][j] = p1.weights[index][j].copy()

    return weights1, weights2