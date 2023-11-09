#training import
import gym
import ray
import ray.tune as tune
from ray.rllib.algorithms.ppo import PPO
from run_training import Envir
from sky130_nist_tapeout import single_build_and_simulation

import argparse
#
#training set up
parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint_dir', '-cpd', type=str)
args = parser.parse_args()
ray.init(num_cpus=33, num_gpus=0,include_dashboard=True, ignore_reinit_error=True)

#configures training of the agent with associated hyperparameters
config_train = {
            #"sample_batch_size": 200,
            "env": Envir,
            "train_batch_size": 1000,
            #"sgd_minibatch_size": 1200,
            #"num_sgd_iter": 3,
            #"lr":1e-3,
            #"vf_loss_coeff": 0.5,
            #"rollout_fragment_length":  63,
            "model":{"fcnet_hiddens": [64, 64]},
            "num_workers": 32,
            "env_config":{"generalize":True, "run_valid":False, "horizon":20},
            }

#Runs training and saves the result in ~/ray_results/train_ngspice_45nm
#If checkpoint fails for any reason, training can be restored
trials = tune.run(
    "PPO", #You can replace this string with ppo.PPOTrainer if you want / have customized it
    name="new_train_with_new_params_3", # The name can be different.
    stop={"episode_reward_mean": 12, "training_iteration": 12},
    checkpoint_freq=1,
    config=config_train,
)
#
