import math
import random
import operator


class Ga():
	def __init__(self,length,count):
		self.length = length
		self.count = count
		self.population = self.gen_population(length,count)

              # create the init chromosome
	def evolve(self,retain_rate=0.8,random_select_rate=0.5,mutation_rate=0.01):
		parents = self.selection(retain_rate,random_select_rate)
		# print len(parents)
		self.crossover(parents)
		self.mutation(mutation_rate)

	def gen_chromosome(self,length):
		chromosome = 0
		for i in xrange(length):
			chromosome |=((1<<i)*random.randint(0,1))
		return chromosome
             # create the population
	def gen_population(self,length,count):
		population = [self.gen_chromosome(length) for i in xrange(count)]
		return population

	def decode(self,chromosome):
		return chromosome * 9.0/(2**self.length-1)

	def calculate_fitness(self,chromosome):
		x = self.decode(chromosome)
		fitness = x + 10*math.sin(5*x) + 7*math.cos(4*x)
		return fitness
             # choose the parents and the lucky ones
	def selection(self,retain_rate, random_select_rate):
		grade = [(self.calculate_fitness(chromosome),chromosome) for chromosome in self.population]
		# print len(grade)
		grade = [x[1] for x in sorted(grade,reverse = True)]
		retain_length = int(len(grade)*retain_rate)
		# choose the good parent
		parents = grade[:retain_length]
		# print len(parents)
		# choose the lucky ones which can't be parents
		for chromosome in grade[retain_length:]:
			if random.random() < random_select_rate:
				parents.append(chromosome)
		return parents

             # cross the parents
	def crossover(self,parents):
		children = []
		print len(self.population)
		target_children_count = len(self.population) - len(parents)
		while len(children) <target_children_count:
			male_num = random.randint(0,len(parents)-1)
			female_num  = random.randint(0,len(parents)-1)
			if male_num != female_num:
				cross_position = random.randint(0,self.length)
				mask = 0
				for i in xrange(cross_position):
					mask |= (1 << i) 
				male = parents[male_num]
				female = parents[female_num]
					# print type(male)
					# print type(mask)
					# print type(male & mask)
					# print type(female & ~mask)
				child = ((int(male) & mask) | (int(female) & ~mask)) & ((1 << self.length) - 1)
				#print child
				children.append(child)
		# print len(parents),len(children)
		self.population = (parents+children)

              # set the mutation 
	def mutation(self,rate):
		for i in xrange(len(self.population)):
			if random.random() < rate:
				j = random.randint(0,self.length-1)
				self.population[i]= int(self.population[i])^(1<<j)

	def get_the_best(self):
		grade = [(self.calculate_fitness(chromosome),chromosome) for chromosome in self.population]
		grade_sorted = [x[1] for x in sorted(grade,reverse=True)]
		the_best_x = ga.decode(grade_sorted[0])
		the_best_y = (the_best_x + 10.0*math.sin(5.0*the_best_x) + 7.0*math.cos(4.0*the_best_x))
		return the_best_x,the_best_y


if __name__ == '__main__':
	ga = Ga(17,300)
	# print len(ga.population)
	for i in xrange(400):
		ga.evolve()
	result = ga.get_the_best()
	print result










               



  










		