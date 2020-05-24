from package_preprocessing import Partition, Departition
from gurobipy import *

def heuristic_generation(scores,conflicts,target_class):


    m = Model('heuristic')
    m.setParam('OutputFlag', False)

    # dummy variable Z
    Z = m.addVar(vtype=GRB.INTEGER, name='Z')

    # I now declare one variable for each possible solution.
    bin = m.addVars(len(scores), vtype=GRB.BINARY, name='bin')


    overlap = m.addConstrs(
        sum([bin[i] for i in conflicts[j]]) == 1 for j in range(len(conflicts))
    )

    opti = m.addConstr(
        Z == sum([bin[i]*scores[i] for i in range(len(scores))])
    )

    desired_class = m.addConstr(
        sum([bin[i] for i in range(len(scores))]) == target_class
    )

    m.setObjective(Z,GRB.MINIMIZE)

    return m



#this function adds classes till the required target is reached
def sub_pack(values):
    end_list = []
    buffer = []
    counter = 0
    lista = values.copy()
    for pair in lista:
        counter += pair[1] * abs(pair[0] - lista[0][0])
        buffer.append(pair)
        end_list.append(
            [
                buffer.copy(),
                counter
            ]
        )
    return end_list

def pack_gen(values,method):
    if method == 'covering':
        lista2 = sorted(values,key=lambda x:x[0]).copy()
    elif method == 'packing':
        lista2 = sorted(values, key=lambda x: x[0], reverse=True).copy()
    else:
        raise ValueError('WRONG METHOD!!!')
    buffer = []
    while len(lista2) > 0:
        buffer += sub_pack(lista2)
        del lista2[0]
    # buffer = [x for x in buffer if x != None]
    # buffer = [tuple(chain for chain  in row) for row in buffer]
    return buffer

def heuristic(method,values,target_class):
# group object into equivalence classes
    partitioned_values = Partition(values)
    print('classes in the initial problem: ', len(partitioned_values))
# list of eq_classes without their cardinality
    eqs = {i[0]:i[1] for i in partitioned_values}
# generate all chains and their loss
    chains = pack_gen(partitioned_values,method)
# define scores for each chain based on how it differs from the target value
    scores = [elem[1] for elem in chains]
# get the list of chains
    items = [elem[0] for elem in chains]
# generate the list of conflicting chains
    conflicts = [[items.index(row) for row in items for elem in row if elem[0] == i] for i in eqs.keys()]
# I call Gurobi to solve the optimization problem
    model = heuristic_generation(scores,conflicts,target_class)
    model.optimize()
    optimum = model.objVal
# solution contains the list of chosen chains
    solution = model.getVars()
    solution = [(x.VarName,x.X) for x in solution]
    solution = [x for x in solution if 'bin' in x[0]]
    solution = [items[i] for i in range(len(solution)) if solution[i][1] == 1]
    solution = [ [pair[0]  for pair in elem] for elem in solution ]
    if method == 'covering':
        new_items = [

            (
                elem[0],
                sum([eqs[chain_el] for chain_el in i])
            )
            for i in solution
            for elem in partitioned_values if elem[0] == min(i)

        ]
    else:
        new_items = [

            (
                elem[0],
                sum([eqs[chain_el] for chain_el in i])
            )
            for i in solution
            for elem in partitioned_values if elem[0] == max(i)

        ]
    print('the new instance has %s classes' % len(new_items))
    # print(new_items)
    num_classes = len(new_items)
    # i need to rearrange the data so that it can be inputed into the RUNNER function
    new_items = Departition(new_items)
    return new_items, num_classes






