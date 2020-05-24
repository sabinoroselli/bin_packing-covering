from package_preprocessing import Partition, fitss
from gurobipy import *
from time import time as tm
import csv

import sys
sys.setrecursionlimit(20000)

# instance = 'benchmark/Falkenauer_t/Falkenauer_t60_00.txt'
# instance = 'benchmark/Hard28/Hard28_BPP13.txt'
instance = 'benchmark/Wascher/Waescher_TEST0005.txt'

# parsing the instance file
with open(instance, mode='r') as in_file:
    reader = csv.reader(in_file, delimiter='\n')
    values = []
    num_items = next(reader)
    target = int(next(reader)[0])
    for i in (reader):
        values.append(int(i[0]))
# partitioning the items into equivalence classes
values_classes = Partition(values)
start_package_gen = tm()

# generating the fit packages
lista = fitss(sorted(values_classes, key=lambda x: x[0], reverse=True).copy(), [], target)
print('package generation: ',tm()-start_package_gen)


start_package_manipulation = tm()
# manipulating the list to make it suitable for the next steps
lista = [[x for x in classe if x[1] > 0] for classe in lista]
lista = [{str(sub[0]): sub[1] for sub in element} for element in lista]
print('package manipulation: ', tm() - start_package_manipulation)

# turning the value_classes list into a dict (for convenience)
values_classes = {str(sub[0]): sub[1] for sub in values_classes}

print('generated_solutions ', len(lista))

# print(lista)
# print(values_classes)


m = Model('packing_eq')
m.setParam('OutputFlag', False)
# m.setParam('TimeLimit', tout)

start_var_gen = tm()
# each variable bin represents a feasible fit package
bin = m.addVars(len(lista), vtype=GRB.INTEGER, name='bin')
print('variable generation: ', tm() - start_var_gen)
start_domain_const = tm()
# it is only possible to pick an positive number of packages
domain = m.addConstrs(bin[i] >= 0 for i in range(len(lista)))
print('domain constraint: ', tm() - start_domain_const)
start_obj_funct = tm()
# set objective function
m.setObjective(quicksum([bin[i] for i in range(len(lista))]), GRB.MINIMIZE)
print('objective function: ', tm()- start_obj_funct)
start_overlap_const = tm()
# it is only possible to have overlapping packages as long as there are enough
# items of each class to form all of them
uni = m.addConstrs(
    values_classes[j]
    <=
    quicksum([
        lista[i_index][j]
        *
        bin[i_index] for i_index in range(len(lista))
        if j in lista[i_index]
    ])
    for j in values_classes
)
print('overlap constraint: ', tm()-start_overlap_const)
# optimizing the model
m.optimize()
print('runtime: ', m.Runtime)
print('objective: ',m.objVal)


