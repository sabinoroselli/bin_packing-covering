from all_in_one import overall,run_existing_instance
import os
# num_obj = 300
# target = 375
# media = 150
# deviazione = 90
# Range = 20
# seme = 9
# tout = 1200
#
# # for Range in range(39, 9, -1):
# overall('covering',
#             'eq',
#             tout,
#             target,
#             num_obj,
#             Range,
#             media,
#             deviazione,
#             seme,
#             heur = False,
#             des_class = 10
#             )
#
#
obs = [200,300,500] # 60,70,80,100,150,

targets = [800,900] # 300,400,500,600,700,

devs = [50] # ,30,50,70,90

seeds = [5,6,7,8,9]

tout = 1200

Range = 20

media = 150


for seed in seeds:
    overall('covering',
            'eq',
            tout,
            900,
            150,
            Range,
            media,
            50,
            seed,
            heur=False,
            )


# set of experiments for the EQUIVALENCE CLASSES model (covering)
for ob in obs:
    for tar in targets:
        for dev in devs:
            for seed in seeds:
                overall('covering',
                        'eq',
                        tout,
                        tar,
                        ob,
                        Range,
                        media,
                        dev,
                        seed,
                        heur=False,
                        )

# set of experiments for the EQUIVALENCE CLASSES model (packing)
for ob in obs:
    for tar in targets:
        for dev in devs:
            for seed in seeds:
                overall('packing',
                        'eq',
                        tout,
                        tar,
                        ob,
                        Range,
                        media,
                        dev,
                        seed,
                        heur=False,
                        )


# sets = ['Falkenauer_t','Falkenauer_u','Scholl_1','Scholl_2','Scholl_3','Schwerin_1','Schwerin_2','Wascher','Hard28']
#
# for instance_set in sets:
#     for instance in sorted(os.listdir('benchmark/{}'.format(instance_set))):
#         run_existing_instance('packing', 'std', 60, instance_set, instance)
#         print(instance)



# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N1C3W1_Q.txt' ) #23.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N1C3W1_L.txt' ) #72.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N1C3W1_M.txt' ) #134.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C2W1_F.txt' ) #200.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C2W1_D.txt' ) #480.000
#
#
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C1W1_O.txt' ) #2.300.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C2W1_T.txt' ) #3.100.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C3W1_B.txt' ) #3.900.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C2W1_K.txt' ) #5.300.000
# run_existing_instance('packing','eq',1200, 'Scholl_1', 'N2C3W1_C.txt' ) #6.000.000
#
# run_existing_instance('packing','eq',1200, 'Scholl_3', 'HARD4.txt' ) #7.000.000
# run_existing_instance('packing','eq',1200, 'Scholl_3', 'HARD1.txt' ) #8.000.000
# run_existing_instance('packing','eq',1200, 'Scholl_3', 'HARD9.txt' ) #9.300.000
