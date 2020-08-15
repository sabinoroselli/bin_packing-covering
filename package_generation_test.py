# from package_preprocessing import Partition, fitss, manipulatedFitss, manipulatedFitssTree
from package_preprocessing import *
from gurobipy import *
from time import time as tm
import csv
import sys
sys.setrecursionlimit(20000)

# instance = 'benchmark/frehage_testInstance.txt'
# instance = 'benchmark/Falkenauer_t/Falkenauer_t60_00.txt'
# instance = 'benchmark/Scholl_1/N3C1W1_A.txt'
# instance = 'benchmark/Schwerin_1/Schwerin1_BPP10.txt'
# instance = 'benchmark/Hard28/Hard28_BPP13.txt'
# instance = 'benchmark/Wascher/Waescher_TEST0005.txt'
instance = 'benchmark/Wascher/Waescher_TEST0022.txt'

print('Package generation test')

# parsing the instance file
print('* Processing instance: ', instance)
with open(instance, mode='r') as in_file:
    reader = csv.reader(in_file, delimiter='\n')
    values = []
    num_items = next(reader)
    target = int(next(reader)[0])
    for i in (reader):
        values.append(int(i[0]))

# partitioning the items into equivalence classes
print('* Partitioning the items into equivalence classes')
values_classes = Partition(sorted(values, reverse=True))
print(values_classes)



# # OLD VERSION	
# print('')
# print('###  OLD GENERATION + MANIPULATION  ###')

# # generating the fit packages
# print('')
# print('* Generating the fit packages')
# start_package_gen = tm()
# lista = fitss(values_classes.copy(), [], target)
# print('  package generation: ', tm() - start_package_gen)
# print('Packages', len(lista))
# print('Example: ', lista[0])


# # manipulating the list to make it suitable for the next steps
# print('')
# print('* Manipulating the list to make it suitable for the next steps')
# start_package_manipulation = tm()
# lista = [[x for x in classe if x[1] > 0] for classe in lista]
# lista = [{str(sub[0]): sub[1] for sub in element} for element in lista]
# print('  package manipulation: ', tm() - start_package_manipulation)
# print('Packages', len(lista))
# print('Example: ', lista[0])
# # for i in lista:
# # 	print(i)

# print('')
# print('TOTAL TIME: ', 2 * tm() - start_package_gen - start_package_manipulation)




# # NEW VERSION v1
# print('')
# print('###  INTEGRATED GENERATION + MANIPULATION  ###')
# print('')
# start_package_genm = tm()
# listam = manipulatedFitss(values_classes, target)
# print('Packages', len(listam))
# print('Example: ', listam[0])
# for i in range(min(10,len(listam))):
# 	print(listam[i])

# print('')
# print('TOTAL TIME: ', tm() - start_package_genm)




# NEW VERSION v2
print('')
print('###  STORING RESULT AS TREE  ###')
print('')
start_package_genm = tm()
treea = manipulatedFitssTree(values_classes, target)


print('  package generation: ', tm() - start_package_genm)

print('')
print('TOTAL TIME: ', tm() - start_package_genm)


# WANNA VERIFY THE NUMBER OF SOLUTIONS IN THE TREE
def countSolutions(tree):
	if isinstance(tree,int):
		return 1
	else:
		return sum([countSolutions(t) for t in tree])
print(countSolutions(treea))


# # # WANNA SEE WHAT THE TREE LOOKS LIKE?
# # def exploreTree(tree,level=0):
# # 	if isinstance(tree,int):
# # 		print(level*"   ", tree)
# # 	else:	
# # 		for i in range(0, len(tree)):
# # 			print(level*"   ", i)
# # 			exploreTree(tree[i],level+1)
# # exploreTree(treea)




# NEW VERSION v3
print('')
print('###  NOVEL IDEA ON WHAT PACKAGES THAT IS REQUIRED  ###')
print('')


remaining_value = [sum([values_classes[i][0]*values_classes[i][1] for i in range(j+1,len(values_classes))]) 
    for j in range(len(values_classes))]

start_package_genm = tm()
listam = fitterPackageGeneration(values_classes, remaining_value, target)
print('Packages', len(listam))
print('Example: ', listam[0])
for i in range(min(10,len(listam))):
    print(listam[i])

print('')
print('TOTAL TIME: ', tm() - start_package_genm)
