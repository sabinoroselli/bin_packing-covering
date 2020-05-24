BIN PACKING/COVERING SCHEDULER

In order to work with the solver, it is necessary to have Gurobi installed on the machine

Additional python packages such as "numpy", "scipy", "os", "csv", "re" are required (installing Anaconda is probably the quickest way to get all of them at once)

The "bin scheduler" allow to allocate items into bins and it works both for packing (when bins have a maximum capacity and the goal is to minimize the number of bins that contain all items) and covering (or dual-packing, where bins have a minimum target and the goal is to maximize the number of bins)

The scheduler can generate instances with normally distributed items based on parameters such as range of values, number of items, target value and distribution specifications such as average value and deviation, or read existing instances from csv files (sets of benchmark instances from the literature are available in the benchmark forlder). 

It is possible to solve instances using the standard ILP formulation from the literature 'STD' (see Kantorovich: Mathematical methods of organising and planning production) or with the equivalence class method 'EQU'. All four models are stored in the file 'models.py'
 
When using the EQU, it is necessary to generate package classes in order to build the model (seee our work: On the Use of Equivalence Classes for Optimal and Sub-Optimal Bin Covering). This is taken care of by the functions in the 'package_preprocessing.py' file for both covering (skinnies) and packing (fitss). 

It is also possible to simplify the instance by merging equivalence classes, so that both the package generation and the actual model solving become much faster. In this case the solution will be a suboptimal one. The functions to accomplish this are in the 'heur_fun.py' file. 

The file 'instance_runner.py' contains the functions to either generate an instance or to parse it from a csv file and then run it after choosing the model.

The file 'all_in_one.py' allows to write the data related to the instance run on a log file (time measured for the different sub-functions, optimal value, nuber of generated packages, etc...)

Finally, the file 'interface.py' shows some example of function calls to run several instances at once.
