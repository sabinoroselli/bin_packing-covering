import numpy as np
import scipy.stats as stats
from package_preprocessing import Partition,skinnies,fitss
from models import covering_eq_class,\
                   covering_standard,\
                   packing_standard,\
                   packing_eq_class
from time import time as tm
import matplotlib.pyplot as plt
import csv

# if i already have an instance to evalueate in a txt file, i can parse it with this function
def instance_parser(instance):
    with open(instance,mode='r') as in_file:
        reader = csv.reader(in_file,delimiter='\n')
        values = []
        num_items = next(reader)
        target = int(next(reader)[0])
        for i in (reader):
            values.append(int(i[0]))
        print('the sum of all items in the instance', sum(values))
        info_values = Partition(values.copy())
        print('#_eq_classes', len(info_values))
        average_lenght = round(np.average([x[1] for x in info_values]), 2)
        print('average class size', average_lenght)
        return values,average_lenght,len(info_values),target

# this function generates an instance given the parameters
def generator(num_obj, minimo, massimo, media, deviazione, seme, show = False):
    np.random.seed(seme)
    dist = stats.truncnorm(
        (minimo - media) / deviazione,
        (massimo - media) / deviazione,
        loc=media, scale=deviazione
    )
    values = dist.rvs(num_obj).astype(int)
    print('the sum of all items in the instance',sum(values))
    info_values = Partition(values.copy())
    print('#_eq_classes', len(info_values))
    average_lenght = round(np.average([x[1] for x in info_values]),2)
    print('average class size', average_lenght)
    # the following set of commands can plot the distribution on an histogram
    # print('generated values',values)
    if show == True:
        print(values)
        plt.hist(values)
        plt.show()

    return values,average_lenght, len(info_values)

# this function runs the different models
def runner(method,model,target,values,tout):
    num_obj = len(values)
    measurements = {'optimum':'None',
                    'generation':'None',
                    'model':'None',
                    'pack_gen':'None',
                    '#_eq_classes': 'None',
                    '#_packages': 'None'
                    }
    # here i generate the instance
    if model == 'std':
        start_mod_gen = tm()
        if method == 'covering':
            standard = covering_standard(num_obj, target, values,tout)
        elif method == 'packing':
            standard = packing_standard(num_obj, target, values,tout)
        else:
            raise ValueError('WRONG METHOD!!!')
        end_mod_gen = tm() - start_mod_gen
        start_model = tm()
        standard.optimize()
        end_model = tm() - start_model
        optimum = standard.objVal
        # print('optimum: ', optimum)
        # print('solving time: ', end_model)
    elif model == 'eq':
        # i am now generating the equivalence classes out of the values
        values_classes = Partition(values)
        measurements.update({'#_eq_classses': len(values_classes)})
        # generating the list of packages and rearranging the data structure
        start_package_gen = tm()
        if method == 'covering':
            lista = skinnies(sorted(values_classes, key=lambda x: x[0], reverse=True).copy(), [], target)
        elif method == 'packing':
            lista = fitss(sorted(values_classes, key=lambda x: x[0], reverse=True).copy(), [], target)
        else:
            raise ValueError('WRONG METHOD!!!')
        lista = [[x for x in classe if x[1] > 0] for classe in lista]
        lista = [{str(sub[0]): sub[1] for sub in element} for element in lista]
        # for i in lista:
        #     print(i)
        values_classes = {str(sub[0]): sub[1] for sub in values_classes}
        print('generated_solutions ', len(lista))
        end_package_gen = tm() - start_package_gen
        measurements.update({'pack_gen':end_package_gen})
        measurements.update({'#_packages':len(lista)})
        # now i am running the equivalence class model
        start_mod_gen = tm()
        if method == 'covering':
            equivalence = covering_eq_class(lista,values_classes,tout)
#             comment on this line if you want to print the lp model in a separate file (can be useful to check the single constraints)
#             equivalence.write('model.lp')
        elif method == 'packing':
            equivalence = packing_eq_class(lista,values_classes,tout)
        else:
            raise ValueError('WRONG METHOD!!!')
        end_mod_gen = tm() - start_mod_gen
        start_model = tm()
        equivalence.optimize()
        # variables = equivalence.getVars()
        # for i in variables:
        #     print(i)
        end_model = tm() - start_model
        optimum = equivalence.objVal
        print('package generation time: ',end_package_gen)
    else:
        raise ValueError('WRONG MODEL!!!')
    print('optimum: ', optimum)
    print('model generation: ', end_mod_gen)
    print('solving time: ', end_model)
    measurements.update({'model': end_model})
    measurements.update({'optimum': optimum})
    measurements.update({'generation': end_mod_gen})
    return measurements

