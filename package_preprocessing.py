# the following three functions are rutines used to make the actual functions more readable and compact
def divceil(div, num):
    return (div + num - 1) // num


def concat(xss):
    return [x for xs in xss for x in xs]


# like append, but pure
def snoc(xs, x):
    res = xs.copy()
    res.append(x)
    return res


# this functions generates the list of skinny packages out of a list of equivalence classes
def skinnies(vms, partial, target):
    vm = vms.pop(0)
    v, m = vm[0], vm[1]
    c = max([(target + v - 1) // v, 0])

    if len(vms) == 0 and c <= m:
        partial.append((v, c))
        return [partial.copy()]
    elif len(vms) == 0:
        return []
    else:
        return concat(
            [skinnies(vms.copy(), snoc(partial, (v, d)), target - d * v) for d in range(0, min(m + 1, c + 1))])


# adds the key value to new dict
def updatePartial(partial, v, c):
    if c == 0:
        return partial
    else:
        res = partial.copy()
        res[str(v)] = c
        return res




# this functions generates the list of fit packages out of a list of equivalence classes
# ISSUE: generates incorrect packages with a too high number of minimum items. Does this really make sense?
def fitss(vms, partial, target):
    vm = vms.pop(0)
    v, m = vm[0], vm[1]
    c = max([target // v, 0])

    if len(vms) == 0:
        partial.append((v, c))
        return [partial.copy()]
    else:
        return concat(
            [fitss(vms.copy(), snoc(partial, (v, d)), target - d * v) for d in range(0, min(m + 1, c + 1))])




# An upgrade to fitss(vms, partial, target)
# Major changes:
# - uses indices instead of list manipulation for the vms
# - generates the manipulated version directly, i.e. only includes nonzero classes as as dict.s
def manipulatedFitss(vms, target, index=0, partial={}):
    vm = vms[index]   # I reverse the order of pop since pop() has complexity O(1)
    v, m = vm[0], vm[1]
    c = target // v

    if index == len(vms) - 1:
        # if c <= m:
        return [updatePartial(partial, v, c)]
        # else:
        #     return []
    else:
        return concat(
            [manipulatedFitss(vms, target - d * v, index=index + 1, partial=updatePartial(partial, v, d)) for d in range(0, min(m + 1, c + 1))])




# An upgrade to manipulatedFitss(vms, partial, target)
# Major changes:
# - uses a tree stucture to store the bins
def manipulatedFitssTree(vms, target, i=0):
    vm = vms[i]   # I reverse the order of pop since pop() has complexity O(1)
    v, m = vm[0], vm[1]
    c = target // v

    if i == len(vms) - 1:
        return c
    else:
        return [manipulatedFitssTree(vms, target - d * v, i=i + 1)
            for d in range(0, min(m + 1, c + 1))]




# An upgrade to manipulatedFitss(vms, partial, target)
# Major changes:
# - does not add virtual items, instead it added second smallest items and then thrid smallest items and so on
def fitterPackageGeneration(vms, rem, target, index=0, partial={}):
    vm = vms[index]   # I reverse the order of pop since pop() has complexity O(1)
    v, m = vm[0], vm[1]
    c1 = max(0, (target - rem[index]) // v)
    c2 = min(m, target // v)

    if index == len(vms) - 1:
        # if target - m * v < vms[0][0]:
        return [updatePartial(partial, v, c2)]
        # else:
        #     print(updatePartial(partial, v, c2))
        #     return []
    else:
        return concat(
            [fitterPackageGeneration(vms, rem, target - d * v, index=index + 1, partial=updatePartial(partial, v, d)) for d in range(c1, c2 + 1)])




# this recursive function generates a list of equivalence classes (and their cardinality) out of a list of items
def Partition(lista):
    eq_class = []

    def partition(lista):
        if lista != []:
            trues = []
            falses = []
            for i in lista:
                if i == lista[0]:
                    trues.append(i)
                else:
                    falses.append(i)
            eq_class.append(trues)
            partition(falses)
    partition(lista)
    eq_class = [(j[0], len(j)) for j in eq_class]

    return eq_class


def Departition(lista):
    values = []

    def subDepa(lista2):
        return [lista2[0][0] for _ in range(lista2[0][1])]
    while len(lista) > 0:
        values += subDepa(lista)
        del lista[0]
    return values
