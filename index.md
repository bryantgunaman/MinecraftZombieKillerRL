https://bryantgunaman.github.io/MinecraftZombieKillerRL/
## Minecaft: Zombie Killer RL

Team Members: Bryant Gunaman (21268398), Rafael Tuazon (31238954),  George Zhong (17744349) 

### Project Summary

  Zombie Killer is a Minecraft bot that we are going to train to kill zombies. To teach our bot, we begin by placing him in a small, flat, bounded environment equipped with weapons (melee and ranged weapons).  When we spawn our bot,  we will also spawn a zombie. As our bot becomes smarter, we will increase the number of zombies and their difficulties. 

  Furthermore, we will also iteratively increase the area of the environment and place obstacles. To prevent our bot from jumping into water bodies to kill zombies, we decided to start with environments that contain no water bodies. 
  
  Ultimately, we are committed to training a bot that is capable of killing any number of zombies given any environments. If our bot learns faster than expected, we will extend to having our bot start with no weapon and train him to build weapons that will help him kill zombies.
  
  The main tools we will use are Minecraft, Malmo and Curriculum Learning.

### Evaluation Plan

We are currently at the planning stage of our project. While we are going to suggest several metrics to evaluate our project, they are subject to change depending on how our project progresses. For now the basic rewards should be given as the agent had maintained/improved his health status for a certain amount of time (say 1 hour in the game), had killed a zombie; possible actions for the agent should be movements to 8 directions, searching through the toolbar and using/consuming items (attacking or eating foods); we will keep tracking the agent’s health status and the number of zombies.


```markdown
## Quantitative Evaluation:

- To assess the ability to kill:
	We will start with one easy zombie, then iteratively increase the number of zombies up to ten. When our bot can kill ten easy zombies, we will conclude that our bot is capable of killing.

- To assess the ability to fight:
	We will start with one easy zombie, then iteratively increase the difficulty to hard. When our bot can kill three hard zombies, we will conclude that our bot is capable of fighting.

## Qualitative Analysis:

- To assess the ability to fight and kill:
	We will randomize our maps, bot spawn locations, and zombie spawn locations. If our bot can consistently kill zombies in randomized environments, we conclude that our bot can fight and kill.

- To assess the ability to use different weapons:
    We will test our bot to use melee and ranged weapons separately. If our bot is capable of killing zombies regardless of the type of weapon they are using, we conclude that it can use different weapons.

- To assess the ability to heal:
	If when the bot's health is low, it consistently uses items that zombies dropped to heal himself, we conclude that our bot can heal.
```

```markdown
## Goals

**Milestone 1 (Minimum):**

1) Be able to fight and kill zombies
2) Use melee and ranged weapons to kill zombies

Implemented Q-Table learning agent from `hit_test.py`, giving the agent three possible actions: 'moving towards the zombie', 'moving away from the zombie' and 'attack once'. In a 10 by 10 grid area, given a diamond sward and fixed initial coordinates (for our agent and the zombie), our agent is capable of learning how to kill the zombie and survive from each iteration.

Instructions:

- Run the game ~/Minecraft/launchClient.sh 
- Run the training script ~/Python_Examples/kill_zombie.py

Updated by Feb, 7th, 2020.


**Milestone 2 (Realistic):**

1) Survive through a night regardless of the environment (zombie quantity, zombie difficulty, types of worlds)
2) Be able to use loots from zombies to heal

**Milestone 3 (Ambitious):**

1) Be able to build weapons and gather resources at day time to prepare against surviving against zombies at night
2) Be able to use ranged typed weapons.
```

## Appointment with Instructor
Appointment reserved for 1:00pm - 1:15pm, Tuesday, January 28, 2020
