from random import uniform, sample
from operator import attrgetter

def fps(pop):
    # Sum total fitnesses
    if pop.optim == 'max':
        
        total_fitness = sum([i.fitness for i in pop])
        
    else:
        
         total_fitness = sum([1/i.fitness for i in pop])
         
    # Get a 'position' on the wheel
    spin = uniform(0, total_fitness)
    position = 0
    # Find individual in the position of the spin
    for individual in pop:
        
        if pop.optim == 'max':
            
            position += individual.fitness
            
        else:
            
            position += 1 / individual.fitness
            
        if position > spin:
            return individual


def tournament(pop, size):
    # Select individuals based on tournament size
    tournament = sample(pop.individuals, size)
    # Return the fittest inividuals from the sample
    if pop.optim == 'max':
        
        return max(tournament, key=attrgetter("fitness"))
    
    else:
        
         return min(tournament, key=attrgetter("fitness"))


def ranking(pop):
    # Create a ranking list
    rank_list = list(range(1, len(pop)+1))
    # Sort the individuals according to their fitness values
    if pop.optim == 'max':
        sorted_indivs = sorted(pop, key=attrgetter("fitness")) #ascending
    else:
        sorted_indivs = sorted(pop, key=attrgetter("fitness"), reverse = True) #descending
    # Merge both in a list of tuples
    ranking = [(rank_list[i], sorted_indivs[i]) for i in range(1, len(pop))] 
    # Get a 'position' on the wheel
    spin = uniform(0, sum(rank_list))
    position = 0
    # Find individual in the position of the spin
    for ind_rank in ranking:
        ranking = ind_rank[0]
        individual = ind_rank[1]
        position += ranking
        if position > spin:
            return individual


    
            
                


