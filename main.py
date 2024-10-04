from music_generation import generate_initial_population
from evolutionary_functions import paretoSelection, uniformCrossOver, mutatePiece
from music_conversion import Lilypond
from fitness import all_default_tests
import music_file
from config import configGenetic
import graph

import random

if __name__ == "__main__":
	#generate inital sorted population
	newPopulation = generate_initial_population(configGenetic)
	newPopulation.sort(key = lambda x: x[1]["overall_score"], reverse=True)

	unsuccessfulGenerations = 0
	bestCandidateScore = newPopulation[0][1]["overall_score"]

	#repeat workflow until no improvement is found in newerGenerations
	while unsuccessfulGenerations < configGenetic["terminationNumber"]:
		#copy previous population into this generations "oldPopulation"
		oldPopulation = newPopulation
		newPopulation = []

		#add elites into new population
		for i in range(configGenetic["numberElites"]):
			newPopulation.append(oldPopulation[i])

		while len(newPopulation) <= configGenetic["terminationNumber"]:
			#selection parents from previous population
			parent1, parent2 = paretoSelection(oldPopulation)
			#do crossover on parents to create children (only note array of children)
			child1, child2 = uniformCrossOver(parent1[0]["noteArray"], parent2[0]["noteArray"])

			#percent chance to mutate either child (only note array of children)
			if 1 <= configGenetic["mutationChance"]:
				mutatePiece(child1)
			if random.randint(1,100) <= configGenetic["mutationChance"]:
				mutatePiece(child2)

			#assumes standard consistent musical characteristics
			child1 = {
						"bars" : configGenetic["numberBars"],
						"keySig" : ["C", "major"],
						"clef" : "treble",
						"timeSig" : [4, 4],
						"noteArray": child1
						}
			child2 = {
						"bars" : configGenetic["numberBars"],
						"keySig" : ["C", "major"],
						"clef" : "treble",
						"timeSig" : [4, 4],
						"noteArray": child2
						}
			
			child1Fitness = all_default_tests(child1)
			child2Fitness = all_default_tests(child2)

			#add children to end of newPopulation in correct format
			newPopulation.append([child1, child1Fitness])
			newPopulation.append([child2, child2Fitness])
		
		newPopulation.sort(key = lambda x: x[1]["overall_score"], reverse=True)

		#if there is no improvement to bestCandidate, then new generation is unsuccessful
		bestNewGenScore = newPopulation[0][1]["overall_score"]
		if bestCandidateScore == bestNewGenScore :
			unsuccessfulGenerations += 1
		else: 
			unsuccessfulGenerations = 0
			bestCandidateScore = bestNewGenScore 

	#best Candidate is first item in newPopulation which is sorted by overall_fitness_score
	bestCandidate = newPopulation[0]

	#Lilypond(bestCandidate[0])


	#draw graph of created file
	graph.draw()