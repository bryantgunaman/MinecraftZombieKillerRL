# MinecraftZombieKillerRL
https://bryantgunaman.github.io/MinecraftZombieKillerRL/

Team Members: Bryant Gunaman (21268398), Rafael Tuazon (31238954),  George Zhong (17744349) 

### Project Summary

  Our project aims to train a Minecraft agent to kill all zombies presented to it. The agent should actively look for zombies to kill whenever possible, and evade zombies in situations that they might die. There are some commands that the agent needs to know and use at the right times. However, simply using commands at the correct times is not enough. When fighting multiple zombies, being damaged is almost inevitable. Therefore, it is also essential that our  agent is capable of healing itself. 
  
  The main tools we will use are Minecraft Malmo, Keras Tensorflow, Python3, TKInterface, and Numpy.

### Evaluation Plan

The project is divided into three milestones. Milestone 1 consists of the agent being able to kill a zombie. We have completed Milestone 1 successfully with 
h our Tabular Q Learning and Deep Q Network Models. Milestone 2 consists of the agent being able to kill multiple zombies and heal itself; this is still a work in progress. Milestone 3 is an ambitious milestone which aims to train the agent to collect materials to build weapons in the day, and use the built weapons to kill zombies at night. 


## Quantitative Evaluation:

- To assess the ability to kill:
	We will start with one easy zombie, then iteratively increase the number of zombies up to three. When our agent can kill three zombies, we will conclude that our agent is capable of killing.

- To assess the ability to fight:
	We will start with one easy zombie, then iteratively increase the difficulty to hard. When our agent can kill three hard zombies, we will conclude that our agent is capable of fighting.

## Qualitative Analysis:

- To assess the ability to fight and kill:
	We will randomize our maps, agent spawn locations, and zombie spawn locations. If our agent can consistently kill zombies in randomized environments, we conclude that our agent can fight and kill.

- To assess the ability to heal:
	If when the agent's health is low, it consistently uses items that zombies dropped to heal himself, we conclude that our agent can heal.



## Goals

**Milestone 1 (Minimum):**

1) Be able to fight and kill zombies
2) Use melee and ranged weapons to kill zombies

Implemented Q-Table learning agent from `hit_test.py`, giving the agent three possible actions: 'moving towards the zombie', 'moving away from the zombie' and 'attack once'. In a 10 by 10 grid area, given a diamond sward and fixed initial coordinates (for our agent and the zombie), our agent is capable of learning how to kill the zombie and survive from each iteration.

Instructions:

- Install the required dependencies:
```
pip install numpy
pip install matplotlib
pip install tensorflow
pip install keras
```
- Set up your MalmoXSD path
- Run the game ~/Minecraft/launchClient.sh 
- Run the training script ~/ZombieKiller/main_keras.py


**Milestone 2 (Realistic):**

1) Be able to consistently kill multiple zombies.
2) Be able to heal at the right timings.

**Milestone 3 (Ambitious):**

1) Be able to build weapons and gather resources at day time to prepare against surviving against zombies at night
2) Be able to use ranged typed weapons.

***Presentation Link: https://tinyurl.com/swdb3u9***

