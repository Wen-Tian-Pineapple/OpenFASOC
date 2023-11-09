# Machine Learning Optimization
Code for reinforcement learning loop with openfasoc generators for optimizing metrics

## Code Setup
The code is setup as follows:

The top level directory contains two sub-directories:
* model.py: top level RL script, used to set hyperparameters and run training
* run_training.py: contains all OpenAI Gym environments. These function as the agent in the RL loop and contain information about parameter space, valid action steps and reward.
* eval.py: contains all of the code for evaluation
* gen_spec.py: contains all of the random specification generation

## Training
Make sure that you have OpenAI Gym and Ray installed. To do this, run the following command:

To generate the design specifications that the agent trains on, run:
```
python3.10 gen_specs.py
```
The result is a yaml file dumped to the ../generators/gdsfactory-gen/.

To train the agent, open ipython from the top level directory and then: 
```
python3.10 model.py
```
The training checkpoints will be saved in your home directory under ray\_results. Tensorboard can be used to load reward and loss plots using the command:

```
tensorboard --logdir path/to/checkpoint
```

## Validation
The evaluation script takes the trained agent and gives it new specs that the agent has never seen before. To generate new design specs, run the gen_specs.py file again with your desired number of specs to validate on. To run validation:

```
python3.10 eval.py
``` 

The evaluation result will be saved to the ../generators/gdsfactory-gen/.

## Results
Please note that results vary greatly based on random seed and spec generation (both for testing and validation). An example spec file is provided that was used to generate the results below. 

<p float="left">
  <img src="mean_reward_versus_step.png" width="400" /> 
</p>
