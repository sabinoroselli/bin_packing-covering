# the following three functions are rutines used to make the actual functions more readable and compact

def divceil(div, num):
  return (div + num - 1) // num

def concat(xss):
  return [x for xs in xss for x in xs]

# like append, but pure
def snoc(xs,x):
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

# this functions generates the list of fit packages out of a list of equivalence classes


def fitss(vms, partial, target):
    vm = vms.pop(0)
    v, m = vm[0], vm[1]
    c = max([target // v, 0])

    if len(vms) == 0:
        partial.append((v, c))
        return [partial.copy()]
    else:
        return concat(
            [fitss(vms.copy(), snoc(partial, (v,d)), target - d * v) for d in range(0, min(m + 1, c + 1))])

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
    eq_class = [(j[0],len(j)) for j in eq_class]

    return eq_class

def Departition(lista):
    values = []
    def subDepa(lista2):
        return [lista2[0][0] for _ in range(lista2[0][1])]
    while len(lista) > 0:
        values += subDepa(lista)
        del lista[0]
    return values
