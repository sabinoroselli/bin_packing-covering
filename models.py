from gurobipy import *

def covering_eq_class(filtered_obs,eq_class,tout):

    m = Model('covering_eq')
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', tout)

    bin = m.addVars(len(filtered_obs), vtype=GRB.INTEGER, name='bin')

    domain = m.addConstrs(bin[i] >= 0 for i in range(len(filtered_obs)))

    uni = m.addConstrs(
        eq_class[j]
        >=
        quicksum([
            filtered_obs[i_index][j]
            *
            bin[i_index] for i_index in range(len(filtered_obs))
            if j in filtered_obs[i_index]
        ])
        for j in eq_class
    )

    m.setObjective(quicksum([bin[i] for i in range(len(filtered_obs))]), GRB.MAXIMIZE)

    return m

def packing_eq_class(filtered_obs,eq_class,tout):

    m = Model('packing_eq')
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', tout)

    # each variable bin represents a feasible fit package
    bin = m.addVars(len(filtered_obs), vtype=GRB.INTEGER, name='bin')
    # it is only possible to pick an positive number of packages
    domain = m.addConstrs(bin[i] >= 0 for i in range(len(filtered_obs)))
    # it is only possible to have overlapping packages as long as there are enough
    # items of each class to form all of them
    uni = m.addConstrs(
        eq_class[j]
        <=
        quicksum([
            filtered_obs[i_index][j]
            *
            bin[i_index] for i_index in range(len(filtered_obs))
            if j in filtered_obs[i_index]
        ])
        for j in eq_class
    )

    m.setObjective(quicksum([bin[i] for i in range(len(filtered_obs))]), GRB.MINIMIZE)

    return m

def covering_standard(num_obj,min_capacity,obs,tout):

    m = Model('covering_standard')
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', tout)

    Z = m.addVar(vtype=GRB.INTEGER, name='Z')

    # this variable keeps track of how full a bin is
    bin = m.addVars(num_obj, vtype=GRB.BINARY, name='bin')
    # bin = m.addVars(num_obj, vtype=GRB.CONTINUOUS, name='bin')

    # this variable becomes one if object i is allocated to bin j
    allo = m.addVars(num_obj, num_obj, vtype=GRB.BINARY, name='allo')
    # allo = m.addVars(num_obj, num_obj, vtype=GRB.CONTINUOUS, name='allo')

    # each object can only be allocated to one bin
    uniqueness = m.addConstrs(sum([allo[i, j] for j in range(num_obj)]) == 1 for i in range(num_obj))

    # if a bin is used, the total weight of the objects inside it must be at least "min_capacity"
    threshold = m.addConstrs(
        sum([
            allo[i, j] * obs[i] for i in range(num_obj)
        ])
        >=
        bin[j] * min_capacity
        for j in range(num_obj)
    )

    # the objective function to maximize is the sum of the used bins
    opti = m.addConstr(Z == sum([bin[i] for i in range(num_obj)]))


    m.setObjective(Z, GRB.MAXIMIZE)

    return m

def packing_standard(num_obj,max_capacity,obs,tout):

    m = Model('packing_standard')
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', tout)

    # objective function
    Z = m.addVar(vtype=GRB.INTEGER,name='Z')


    # this variable is used to decide whether a bin is used or not
    bin = m.addVars(num_obj, vtype=GRB.BINARY, name='bin')

    # this variable is used to decide whether object i is assigned to bin j
    allo = m.addVars(num_obj,num_obj, vtype = GRB.BINARY, name='allo')

    # objective function setting
    opti = m.addConstr( Z == sum([bin[i] for i in range(num_obj)]))

    # at least one bin must be chosen (do i really need it?)
    at_least_one = m.addConstr(Z >= 1)

    # each object must be assigned exactly to one bin
    uniqueness = m.addConstrs(sum([
                allo[i,j] for j in range(num_obj)
            ]) == 1
        for i in range(num_obj)
    )

    # if a bin is chosen, the cumulative value it contains cannot exceed the target value
    max_value = m.addConstrs(
        sum([
            allo[i,j] * obs[i] for i in range(num_obj)
        ]) <= max_capacity * bin[j]
    for j in range(num_obj)
    )

    m.setObjective(Z, GRB.MINIMIZE)

    return m


