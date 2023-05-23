"""
    Adaptation from
    https://github.com/kiecodes/genetic-algorithms
"""
from typing import List, Callable,Tuple
from random import choices, randint, randrange, random
from functools import partial
import time
import itertools
import json

"""-------------DISABLED BECAUSE THESE ARE IMPORTED FROM THE TRANSFER FUNCTION"""
# from courseListCreator import *
# from sessionListCreator import *
"""-------------------------------------------------------------------------"""

from .SessionAssign import classroom_capacity

from .Transfer import *


# Genetic Algorithm constants:
POPULATION_SIZE = 15
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 7
OPTIMAL_FITNESS_SCORE = 1000.00

received_time = 1

MAX_RUNTIME = received_time * 60 *60 # t in secs



GENOME_LENGTH = 40
FLAG = 0
Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], float]
PopulateFunc = Callable[[],Population]
SelectionFunc = Callable[[Population,FitnessFunc],Tuple[Genome,Genome]]
CrossoverFunc  = Callable[[Genome,Genome], Tuple[Genome,Genome]]
MutationFunc = Callable[[Genome],Genome]

FitnessAndTimeTable = {}
GenomeAndFitness = {}



def generate_genome(length: int) ->Genome:
    return choices([0,1], k =length)

def generate_population(size: int,genome_length: int ) ->Population:
    return [generate_genome(genome_length) for _ in range(size)]


def fitness(genome: Genome,ALLSESSIONS,ALLCOURSES,ALLREG) ->float:

    global FLAG
    if FLAG >5:
        persistTTandFitness()
    FLAG +=1

    genome = ''.join(str(bit) for bit in genome)
    print(genome)
    timeTable = Transfer(genome)
    timeTable.setAttibutes()
    timeTable.generateTimetable()
    timeTable.makeplacementPlans()
    timeTable.AllCourses = ALLCOURSES
    timeTable.allSessions = ALLSESSIONS
    timeTable.AllsessionRegistration = ALLREG
    timeTable.ListingofRooms = timeTable.makeRoomListing()
    placementOperation = f"timeTable.{timeTable.placeDict[timeTable.getPlacement()]}()"
    eval(placementOperation)

    print(timeTable.getTimeTable())
    placementCosts = timeTable.costOfAllPlacements
    fitnesScore = 0.0

    for k ,v in placementCosts.items():
        fitnesScore +=sum(v)
    
    FitnessAndTimeTable[fitnesScore] = timeTable.getTimeTable()
    GenomeAndFitness[genome] = fitnesScore
    return fitnesScore

def selection_pair(population:Population, fitness_func: FitnessFunc) ->Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def single_point_crossover(a:Genome,b: Genome) ->Tuple[Genome,Genome]:
    if len(a) != len(b):
        raise ValueError("Genome lengths must be the same")
    
    length = len(a)
    if length < 2:
        return a,b
    
    p = randint(1,length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: Genome, num: int =1,probability: float =P_MUTATION) ->Genome:
    for _ in range(num):
        index = randrange(len(genome)) 
        genome[index] = genome[index] if random() > probability else abs(genome[index] -1)
    return genome

#returns the current population and the number of generations executed
def run_evolution(
        populate_func :PopulateFunc,
        fitness_func : FitnessFunc,
        fitness_requirement :float,
        selection_func : SelectionFunc = selection_pair,
        crossover_func : CrossoverFunc = single_point_crossover,
        mutation_func : MutationFunc = mutation,
        generation_Limit : int = MAX_GENERATIONS
        )->Tuple[Population, int]:

    """Get external Data """

    AllSession,AllRegistration = allData()
    ExternalAllCourses = getAllcourses()



    #create the Population
    population = populate_func()

    start_time = time.time()
    #sort the population by the best performing genome
    for i in range(generation_Limit):
        print(f"Generation {i}")
        # breakpoint()

        population = sorted(population,key = lambda genome: fitness_func(genome,AllSession,ExternalAllCourses,AllRegistration))

        #if optimal fitness is found
        if GenomeAndFitness[population[0]] <= fitness_requirement:
            break

        if (time.time() -start_time) >= MAX_RUNTIME:
            break

        #enable Elitism, get the top 2
        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population,fitness_func) 
            offspring_a,offspring_b = crossover_func(parents[0],parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a,offspring_b]
        
        population = next_generation

    persistTTandFitness()
        
    return population,i

def persistTTandFitness():
    """Write the best 5 timetables and fitness Scores to their respective Files"""
    first_five_tt = list(itertools.islice(FitnessAndTimeTable.values(), 5))

    first_five_keys = list(FitnessAndTimeTable.keys())[:5]

    dicttopass = {}

    counter = 0
    for iea in first_five_tt:
        dicttopass[counter] = iea
        counter +=1

    json_str = json.dumps(dicttopass)

    # Open the file in write mode
    file_name = 'Best_tables.txt'
    with open(file_name, mode='w') as file:

        # Write the data to the CSV file
        file.write(json_str)


    # Open the file in write mode
    file_name = 'CorrespondingFitness.txt'
    with open(file_name, 'w') as file:
        for element in first_five_keys:
            file.write(element + '\n')

population,generation = run_evolution(
                        populate_func=partial(generate_population,POPULATION_SIZE,GENOME_LENGTH),
                        fitness_func=partial(fitness),
                        fitness_requirement=OPTIMAL_FITNESS_SCORE,
                        generation_Limit=MAX_GENERATIONS
                        )

