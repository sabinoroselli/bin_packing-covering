from instance_runner import runner, generator, instance_parser
from heur_fun import heuristic
import os
import csv
import sys

current_dir = os.getcwd()
# print(current_dir)

# I WILL USE THIS FUNCTION IF I NEED TO GENERATE THE INSTANCE MYSELF (GIVEN THE INSTANCE PARAMETERS)
def overall(method, model, tout, target, num_obj, range, media, dev, seme, heur = False, des_class = 1 ):
    print('CURRENT INSTANCE: ',
          method,
          model,
          target,
          num_obj,
          range,
          media,
          dev,
          seme,
          heur,
          des_class)
    # in case i want to log what i print in the different functions
    # sys.stdout = open('%s/instance_log' % current_dir,'+a')

    param = {'method': method,
             'model': model,
             'target': target,
             'num_obj': num_obj,
             'range': range,
             'media': media,
             'dev': dev,
             'seme': seme,
             '#_eq_classes': 'None',
             '#_feasible_packages': 'None',
             'average_lenght': 'None',
             'heur': heur,
             'des_class': des_class,
             '#_simplified_classes': 'None',
             '#_simplified_packages': 'None',
             'optimum': 'None',
             'model_generation': 'None',
             'Time': 'None'
             }
    minimo = media - range
    massimo = media + range

    instance, average, eq_classes = generator(num_obj,minimo,massimo,media,dev,seme)
    param.update({
            'average_lenght': average,
            '#_eq_classes': eq_classes
        })
    if heur == True:
        instance,num_classes = heuristic(method,instance, des_class)
        param.update({'#_simplified_classes': num_classes})
    data = runner(method, model, target, instance, tout)

    if heur == False:
        param.update({'#_feasible_packages': data['#_packages']})
    else:
        param.update({'#_simplified_packages': data['#_packages']})
    param.update({
        'optimum': data['optimum'],
        'model_generation': round(data['generation'],2),
        'Time': round(data['model'],4)
    })

    # sys.stdout.close()

    with open('%s/instance_data' % current_dir,
              'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(param.values())

    return param


# INSTEAD, IF I ONLY NEED TO READ FROM A FILE, I CAN USE THIS INSTANCE
def run_existing_instance(method, model, tout, instance_set, instance, heur = False, des_class = 'None'):

    # in case i want to log what i print in the different functions (otherwise just comment it off)
    # sys.stdout = open('%s/instance_log' % current_dir,'+a')

    print('Current Instance: ', instance)
    values, average_lenght, eq_classes, target = instance_parser('benchmark/{}/{}'.format(instance_set,instance))
    param = {
             'instance':instance.split('.')[0],
             'method': method,
             'model': model,
             'target': target,
             'num_obj': len(values),
             '#_eq_classes': eq_classes,
             '#_feasible_packages': 'None',
             # 'average_lenght': 'None',
             # 'heur': heur,
             # 'des_class': des_class,
             # '#_simplified_classes': 'None',
             # '#_simplified_packages': 'None',
             'optimum': 'None',
             'model_generation': 'None',
             'Time': 'None'
             }
    if heur == True:
        instance,num_classes = heuristic(method,values, des_class)
        param.update({'#_simplified_classes': num_classes})
    data = runner(method, model, target, values, tout)

    if heur == False:
        param.update({'#_feasible_packages': data['#_packages']})
    else:
        param.update({'#_simplified_packages': data['#_packages']})
    param.update({
        'optimum': data['optimum'],
        'model_generation': round(data['generation'],2),
        'Time': round(data['model'],4)
    })

    # sys.stdout.close()

    with open('%s/instance_data' % current_dir,
              'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(param.values())

    return param
