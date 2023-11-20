import numpy as np
from sky130_nist_tapeout import single_build_and_simulation
import yaml
from pathlib import Path

params = {
                  "diffpair_params0" : [1, 8, 1],       
                  "diffpair_params1" : [0.5, 2.1, 0.1],   
                  "diffpair_params2" : [1, 9, 1],
                  "Diffpair_bias0" : [1, 8, 1],
                  "Diffpair_bias1" : [1, 4.5, 0.5],
                  "Diffpair_bias2" : [3, 13, 1],
                  "pamp_hparams0" : [1, 8, 1], 
                  "pamp_hparams1" : [0.5, 2.1, 0.1], 
                  "pamp_hparams2" : [2, 11, 1],
                  "bias0" : [1, 8, 1], 
                  "bias1" : [0.5, 2.1, 0.1], 
                  "bias2" : [3, 13, 1],
                  "bias3" : [2, 4, 1],
                  "half_pload1": [3, 7, 1],
                  "half_pload3": [4, 9, 1],
                  "mim_cap_rows" : [1, 4, 1],
                  }
paramss = []
params_id = list(params.keys())

params_idx = np.array([3, 5, 7, 5, 4, 0, 3, 0, 2, 5, 15, 1, 0, 3, 4, 2])

for value in params.values():
    param_vec = np.arange(value[0], value[1], value[2])
    paramss.append(param_vec)

paramsss = np.array([paramss[i][params_idx[i]] for i in range(len(params_id))])
#param_val = np.array[OrderedDict(list(zip(self.params_id,params)))]

#run param vals and simulate
#cur_specs = OrderedDict(sorted(self.sim_env.create_design_and_simulate(param_val[0])[1].items(), key=lambda k:k[0]))
#2.69966400e+07

#inputparam = np.array([ 9.  , 2.,  6. ,  6.,   2. ,  4.  , 6.,   1. ,  2.  , 3. ,  7.  , 1  ,6.  , 3. ,12.  ,12.  , 3. ,  2. ])

inputparam = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 1.0, 16.0, 6.0, 2.0, 4.0, 0.0, 1.0, 0.0, 12.0, 12.0, 0.0, 2.0])
inputparam[0:3] = paramsss[0:3]
inputparam[3:6] = paramsss[3:6]
inputparam[6:9] = paramsss[6:9]
inputparam[10:14] = paramsss[9:13]
inputparam[20] = paramsss[13]
inputparam[22] = paramsss[14]
inputparam[25] = paramsss[15]

print(inputparam)
print(paramsss)

result = single_build_and_simulation(inputparam,-269)

print(result)
print(result["ugb"]/(result["Ibias_diffpair"]+result["Ibias_commonsource"]))