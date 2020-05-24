BIN PROBLEM SOLVER:

in order to work with the solver, it is necessary to have Gurobi installed on the machine

additional python packages such as "numpy", "scipy", "os", "csv", "re" are required (installing Anaconda is probably the quickest way to get all of them at once)

the file 'interface' shows how to use the function 'overall' which allowes to generate and run instances. 
	to generate an instances, some parameteres have to be specified:
		number of items
		target value
		average
		deviation
		range of value
		seed
		timeout
		
	it is also possible to simplify the instance by setting the value "heur" to True. in this case, the number of desired equivalence classes has to be specified.

the file 'all_in_one' contains the function 'overall' that first generates an instance based on the specified parameters and then runs it with either the standard model
or with the equivalence classes one. it is also possible to decide whether to solve the instance for the covering problem or for the packing one.

the file 'instance_runner' contains the function 'generator' that generates a set of values normally distributed, based on the specified parameters and the function 'runner',
which generates the skinny\fit packages and calls the different models (from the file 'models') and the solver gurobi to solve the instance.  

the file 'heur_fun' contains the functions used to simplify an instance according to the heuristic explained in the paper. it also contains the linear model to find the optimal chains

the file 'package_preprocessing' contains the functions to generate skinny\fit packages, as well as a function to generate equivalence classes out of an isntance. 