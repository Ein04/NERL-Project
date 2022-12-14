import os
import numpy as np
import multiprocess
import itertools

""" https://github.com/Ankur-Deka/SIGS-Grid-Search/blob/master/grid_search/grid_search.py"""
class GridSearch():
    def __init__(self, main_file, args, num_process=30):
        self.main_file = main_file
        self.args = args
        self.arg_names = args.keys()
        self.num_process = num_process

    def call_main(self, args_list):
        for args in args_list:
            # -------- generate string of arguments -------- #
            args_string = ''
            for i, arg_name in enumerate(self.arg_names):
                args_string += ' --{} {}'.format(arg_name, args[i])

            cmd = 'python {}{}'.format(self.main_file, args_string)
            print('cmd', cmd)
            os.system(cmd)

    def run(self):
        print('Get yourself a cup of coffee while I run grid search')

        # -------- convert range args to list -------- #
        for param, val in self.args.items():
            if not (type(val) is dict or type(val) is list):
                raise ValueError(
                    'args should be a list or dictionary. Please refer to README')
            if type(val) is dict:
                low, high, num, scale = val['min'], val['max'], val['num'], val['scale']
                if scale == 'linear':
                    l = list(np.linspace(low, high, num))
                    self.args[param] = l
                elif scale == 'log':
                    l = list(np.logspace(low, high, num))
                    self.args[param] = l

        # -------- get list of all configurations -------- #
        config_list = []  # separate list for each argument
        for arg_name in self.arg_names:
            config_list.append(self.args[arg_name])
        args_list = list(itertools.product(*config_list))

        # -------- divide into equal parts and run -------- #
        num_configs = len(args_list)
        num_process = min(num_configs, self.num_process)
        IDs = np.array_split(np.arange(num_configs), num_process)
        process_list = []

        for i in range(num_process):
            args_list_process = [args_list[ID] for ID in IDs[i]]
            # import ipdb; ipdb.set_trace()
            x = multiprocess.Process(target=self.call_main, args=(args_list_process,))
            x.start()
            process_list.append(x)

        for x in process_list:
            x.join()