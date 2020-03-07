from __future__ import print_function
# import malmo.minecraftbootstrap; malmo.minecraftbootstrap.set_malmo_xsd_path()
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import range
from builtins import object
from malmo import MalmoPython
from simple_dqn_keras import Agent
import json
import logging
import math
import os
import random
import sys
import time
from malmo import malmoutils
import numpy as np
import ctypes
from mission_generator import MissionGenerator
from visualizer import Visualizer
import matplotlib.pyplot as plt
from past.utils import old_div

class MainKeras():

    def __init__(self, missionXML, n_games=500, max_retries=3, starting_zombies=1,
                 XSize=10, ZSize=10, aggregate_episode_every=5,
                 agent_search_resolution=30, load_model=False):
        # keras attributes
        self.n_games = n_games
 
        self._init_logger()

        # keras
        self.n_actions = 4
        self.agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.0005, input_dims=7,
                  n_actions=self.n_actions, mem_size=1000000, batch_size=64, epsilon_end=0.01)
        self._load_dqn_model(load_model)

        self.scores = []
        self.eps_history = []
        self.aggregate_episode_every = aggregate_episode_every

        # qtable
        self.Qtb = {}
        self._load_qtable(load_model)
        self.epsilon = 0.01 # chance of taking a random action instead of the best

        # agent
        self.agent_host = MalmoPython.AgentHost()
        
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(self.agent_host.getUsage())
            exit(1)
    
        # mission
        self.missionXML = missionXML
        # self._validate_mission()

        self.max_retries = max_retries

        #adding clients
        self.my_client_pool = None
        # self._add_starters()
        self._add_default_client()
        
        self.world_state = None
        
        # mission generator
        self.mission_generator = MissionGenerator(self.missionXML)
        self.starting_zombies = starting_zombies
        self.num_zombies = starting_zombies
        self.zombie_difference = 0  # for reward calculation
        self.XSize = XSize
        self.ZSize = ZSize

        # canvas
        self.visual = Visualizer(arena_width=self.XSize, arena_breadth=self.ZSize)

        # direction learner variables
        self.agent_search_resolution = agent_search_resolution
        self.agent_stepsize = 1
        self.agent_turn_weight = 100
        self.agent_edge_weight = -100
        self.agent_mob_weight = -10
        self.agent_turn_weight = 0 # Negative values to penalise turning, positive to encourage.
        self.turning_diff = 0
        
        # for visualization
        self.flash = False
        self.current_life = 0 
        

        # main loop variables
        self.self_x = 0
        self.self_z = 0
        self.current_yaw = 0
        self.ob = None
        self.all_zombies_dead = False
        self.num_heals = 0
        self.life_decrease_penalty = 0
        self.TimeAlive = 0
        self.time_rewards = 0
        self.heal_rewards = 0
        self.move_backwards_reward = 0

    def _init_logger(self):
        self.logger = logging.getLogger(__name__)
        if False: # True if you want to see more information
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def _load_dqn_model(self, load_model):
        if load_model == True:
            self.agent.load_model()
        

    def _load_qtable(self, load_model):
        if load_model == True:
            with open('QTable.txt') as json_file:
                Qtb = json.load(json_file)
            self.Qtb= Qtb

    def _exportQTable(self):
        with open('QTable.txt', 'w') as outfile:
            json.dump(self.Qtb, outfile)

    def _updateQTable( self, reward, current_state ):
        """Change q_table to reflect what we have learnt."""
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.Qtb[self.prev_s][self.prev_a]
        # TODO: what should the new action value be? try to modify my calculate reward method
        new_q = reward
        # assign the new action value to the Q-table
        self.Qtb[self.prev_s][self.prev_a] = new_q

    def _updateQTableFromTerminatingState( self, reward ):
        """Change q_table to reflect what we have learnt, after reaching a terminal state."""
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.Qtb[self.prev_s][self.prev_a]
        # TODO: what should the new action value be?
        new_q = reward
        # assign the new action value to the Q-table
        self.Qtb[self.prev_s][self.prev_a] = new_q

    def _add_default_client(self):
        self.my_client_pool = MalmoPython.ClientPool()
        self.my_client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))

    def _generate_new_mission(self):
        self.mission_generator.restartXML()
        self.xcoords, self.zcoords = self.mission_generator.getCoords(self.XSize, self.ZSize)
        self.mission_generator.drawEntity("Zombie", self.starting_zombies)
        self.mission_generator.randomStart()
        # self.mission_generator.spawnItems()

    def _add_starters(self):
        # self.my_mission.removeAllCommandHandlers()
        self.my_mission.allowAllContinuousMovementCommands()
        self.my_mission.setViewpoint( 0 )
#        self.my_mission.allowAllDiscreteMovementCommands()
        #self.my_mission.requestVideo( 320, 240 )  use default size instead
    
    def _validate_mission(self):
        self.my_mission = MalmoPython.MissionSpec(self.mission_generator.getXML(), True)
        # self.my_mission_record = MalmoPython.MissionRecordSpec()
    
    def _drawBoundaries(self):
        for i in range(len(self.xcoords)):
            self.my_mission.drawLine(self.xcoords[i % len(self.xcoords)] , 4, self.zcoords[i % len(self.xcoords)], self.xcoords[(i+1) % len(self.xcoords)], 4, self.zcoords[(i+1) % len(self.xcoords)], "fence")


    def _retry_start_mission(self):
        self.my_mission_record = MalmoPython.MissionRecordSpec()
        # self.my_mission_record = malmoutils.get_default_recording_object(self.agent_host, 
        #                          "Mission_" + str(len(self.scores)-1))
        for retry in range(self.max_retries):
            try:
                # Attempt to start the mission:
                self.my_mission.forceWorldReset() # force world to reset for each iteration
                self.agent_host.startMission( self.my_mission, self.my_client_pool, 
                                              self.my_mission_record, 0, "ZombieKiller" )
                break
            except RuntimeError as e:
                if retry == self.max_retries - 1:
                    print("Error starting mission",e)
                    print("Is the game running?")
                    exit(1)
                else:
                    time.sleep(2)
        self._get_valid_worldstate()

    def _start_mission(self):
        self._generate_new_mission()
        self._validate_mission()
        self._add_starters()
        self._drawBoundaries()
        self._retry_start_mission()
    
    def _get_valid_worldstate(self):
        # Loop until mission starts:
        print("Waiting for the mission to start ", end=' ')
        self.world_state = self.agent_host.getWorldState()
        while not self.world_state.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            self.world_state = self.agent_host.getWorldState()
            for error in self.world_state.errors:
                print("Error:",error.text)
        print()

    def _assign_observation(self):
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
            self.ob = json.loads(msg)

    def _get_next_observation(self):
        self.world_state = self.agent_host.getWorldState()
        if self.world_state.number_of_observations_since_last_state > 0: 
            msg = self.world_state.observations[-1].text
            return json.loads(msg)
        return self.ob
    
    def _get_position_and_orientation(self):
        if u'Yaw' in self.ob:
            self.current_yaw = self.ob[u'Yaw']
        if u'XPos' in self.ob:
            self.self_x = self.ob[u'XPos']
        if u'ZPos' in self.ob:
            self.self_z = self.ob[u'ZPos']

    def _calculate_turning_difference_from_zombies(self):
        x_pull, z_pull, current_yaw = self._get_diagonal_difference_from_zombies()
        yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
        difference = yaw - current_yaw
        while difference < -180:
            difference += 360
        while difference > 180:
            difference -= 360
        # print("turn differece: ", difference/180.0)
        return difference / 180.0
        
    def _get_diagonal_difference_from_zombies(self):
        if u'entities' in self.ob:
            entities = self.ob["entities"]
            # print(f'Entities: {entities}')
            return self._get_pull_from_entities(entities) 
    
    def _get_pull_from_entities(self, entities):
        # Get our position/orientation:
        if u'Yaw' in self.ob:
            current_yaw = self.ob[u'Yaw']
        if u'XPos' in self.ob:
            self.self_x = self.ob[u'XPos']
        if u'ZPos' in self.ob:
            self_z = self.ob[u'ZPos']
        num_zombie, x_pull, z_pull = 0, 0, 0
        for e in entities:
            if e["name"] == "Zombie":
                num_zombie += 1
                # Each zombie contributes to the direction we should head in...
                dist = max(0.0001, (e["x"] - self.self_x) * (e["x"] - self.self_x) + (e["z"] - self.self_z) * (e["z"] - self.self_z))
                # Prioritise going after wounded sheep. Max zombie health is 20, according to Minecraft wiki...
                weight = 21.0 - e["life"]
                x_pull += weight * (e["x"] - self.self_x) / dist
                z_pull += weight * (e["z"] - self.self_z) / dist
        return x_pull, z_pull, current_yaw

    def _check_num_zombies(self):
        if u'entities' in self.ob:
            num_zombie = 0
            entities = self.ob["entities"]
            for e in entities:
                if e["name"] == "Zombie":
                    num_zombie += 1
            self._update_num_zombies(num_zombie)

    def _update_num_zombies(self, new_num_zombies):
        if new_num_zombies < self.num_zombies:
            self.zombie_difference = self.num_zombies - new_num_zombies
            self.num_zombies = new_num_zombies
            self.num_heals += 1
        else:
            self.zombie_difference = 0

    def _get_current_rewards(self, current_rewards):
        for reward in self.world_state.rewards:
            current_rewards += reward.getValue()
            print(f"INSIDE FOR: {reward.getValue()}")

        # life decrease penalty
        current_rewards += self.life_decrease_penalty
        print("life decrease penalty: " + str(self.life_decrease_penalty))

        # increase time rewards
        self._increase_time_reward()
        current_rewards += self.time_rewards
        print(f"increase_time: {self.time_rewards}")

        # healing rewards
        current_rewards += self.heal_rewards
        print(f"healing rewards: {self.heal_rewards}")
        
        current_rewards += self._kill_zombie_reward()
        # print(f"kill zombie reward: {self._kill_zombie_reward()}")
        current_rewards += self.move_backwards_reward
        current_rewards += self.heal_rewards
        return current_rewards

    def _increase_time_reward(self):
        if "TimeAlive" in self.ob:
            t = self.ob[u'TimeAlive']
            if t > self.TimeAlive:
                self.time_rewards += (t - self.TimeAlive) * .2 # life decrease penalty
                self.TimeAlive = t

    def _kill_zombie_reward(self):
        return self.zombie_difference * 100

    def _move_towards_zombies(self, difference_from_zombie):
        self.agent_host.sendCommand("turn " + str(difference_from_zombie))
        move_speed = 1.0 if abs(difference_from_zombie) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
        self.agent_host.sendCommand("move " + str(move_speed))
        self.turning_diff = 0
        # print("move " + str(move_speed))

    def _move_away_from_zombies(self, difference_from_zombie):
        self.agent_host.sendCommand("turn " + str(difference_from_zombie))
        move_speed = 1.0 if abs(difference_from_zombie) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
        self.agent_host.sendCommand("move -" + str(move_speed))
        self.turning_diff = 0
        # self.move_backwards_reward = -0.45
        # print("move -" + str(move_speed))

    def _attack(self):
        self.agent_host.sendCommand("attack 1")
        self.agent_host.sendCommand("attack 0")
        print('attack')
    
    def _heal(self):
        if self.num_heals > 0:
            if self.current_life <= 14:
                self.heal_rewards += 100
            self.agent_host.sendCommand("chat /effect ZombieKiller instant_health 3")
            if self.ob['Life'] >= 15:
                self.heal_rewards = -20
            else:
                self.heal_rewards = 20
            self.num_heals -= 1
        else:
            self.heal_rewards -= 25

    def _translate_actions(self, action_num, difference_from_zombie):
        if action_num == 0:
            self._move_away_from_zombies(difference_from_zombie)
        elif action_num ==1:
            self._move_towards_zombies(difference_from_zombie)
        elif action_num == 2:
            self._attack()
        elif action_num == 3:
            self._heal()

    def _basic_observation_to_array(self, ob):
        obs_array = []
        obs_array.append(ob['TimeAlive']) if 'TimeAlive' in ob else 0
        obs_array.append(ob['Life']) if 'Life' in ob else 0
        obs_array.append(ob['XPos']) if 'XPos' in ob else 0
        obs_array.append(ob['YPos']) if 'YPos' in ob else 0
        obs_array.append(ob['ZPos']) if 'ZPos' in ob else 0
        return obs_array

    def _complete_observation_to_array(self, observation):
        observation.append(self.num_zombies)
        observation.append(self.turning_diff)
        return np.array(observation)

    def _observation_to_array(self, ob):
        ob = self._basic_observation_to_array(ob)
        return self._complete_observation_to_array(ob)

    def _check_all_zombies_dead(self):
        zombies_alive = False
        if u'entities' in self.ob:
            entities = self.ob["entities"]
            for e in entities:
                if e["name"] == "Zombie":
                    zombies_alive = True
                    break
        if zombies_alive == False:
            print("quitting mission")
            self.agent_host.sendCommand("chat /kill @e")
    
    # parts of direction learner
    def _findUs(self, entities):
        if u'entities' in self.ob:   
            for ent in self.ob['entities']:
                if ent["name"] == 'Zombie':
                    continue
                else:
                    return ent

    def _getBestAngle(self, current_yaw):
        '''Scan through 360 degrees, looking for the best direction in which to take the next step.'''
        if u'entities' in self.ob:   
            us = self._findUs(self.ob['entities'])
            # Normalise current yaw:
            while current_yaw < 0:
                current_yaw += 360
            while current_yaw > 360:
                current_yaw -= 360
            return us,  current_yaw

    def _look_for_best_option(self, us, current_yaw):
        scores=[]
        for i in range(self.agent_search_resolution):
            # Calculate cost of turning:
            ang = 2 * math.pi * (old_div(i, float(self.agent_search_resolution)))
            yaw = i * 360.0 / float(self.agent_search_resolution)
            yawdist = min(abs(yaw-current_yaw), 360-abs(yaw-current_yaw))
            turncost = self.agent_turn_weight * yawdist
            score = turncost

            # Calculate entity proximity cost for new (x,z):
            x = us["x"] + self.agent_stepsize - math.sin(ang)
            z = us["z"] + self.agent_stepsize * math.cos(ang)
            if u'entities' in self.ob:
                for ent in self.ob['entities']:
                    dist = (ent["x"] - x)*(ent["x"] - x) + (ent["z"] - z)*(ent["z"] - z)
                    if (dist == 0):
                        continue
                    weight = 0.0
                    if ent["name"] == 'Zombie':
                        weight = self.agent_mob_weight
                        dist -= 1   # assume mobs are moving towards us
                        if dist <= 0:
                            dist = 0.1
                    score += old_div(weight, float(dist))
                    scores.append(self._calculate_turning_costs(score, x, z))
                scores.append(score)
        return scores 

    def _calculate_turning_costs(self, score, x, z):
        # Calculate cost of proximity to edges
        distRight = (2+old_div(self.XSize,2)) - x
        distLeft = (-2-old_div(self.XSize,2)) - x
        distTop = (2+old_div(self.ZSize,2)) - z
        distBottom = (-2-old_div(self.ZSize,2)) - z
        if distRight > 0:
            score += old_div(self.agent_edge_weight, float(distRight * distRight * distRight * distRight))
        if distLeft > 0:
            score += old_div(self.agent_edge_weight, float(distLeft * distLeft * distLeft * distLeft))
        if distTop > 0:
            score += old_div(self.agent_edge_weight, float(distTop * distTop * distTop * distTop))
        if distBottom > 0:
            score += old_div(self.agent_edge_weight, float(distBottom * distBottom * distBottom * distBottom))
        return score
    
    def _find_best_score_get_angle(self, scores):
        # Find best score:
        i = scores.index(max(scores))
        # Return as an angle in degrees:
        return i * 360.0 / float(self.agent_search_resolution)

    def _process_direction(self):
        us, current_yaw = self._getBestAngle(self.current_yaw)
        scores = self._look_for_best_option(us, current_yaw)
        angle = self._find_best_score_get_angle(scores)
        return angle
    
    def _turn(self):
        if "entities" in self.ob:
            entities = self.ob["entities"]
            best_yaw = self._process_direction()
            difference = best_yaw - self.current_yaw;
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;
            self.agent_host.sendCommand("move 1") 
            self.agent_host.sendCommand("turn " + str(difference))
            self.turning_diff = difference
            # print('turning')
        else:
            self.turning_diff = 0

    def _plot_dqn_results(self, scores, eps_history, filename='zombie_kill.png', lines=None):
        x = [i+1 for i in range(self.n_games)]
        print("Plotting results...")
        self._plotLearning(x, scores, eps_history, filename, lines=None)

    def _plotLearning(self, x, scores, epsilons, filename, lines=None):
        fig=plt.figure()
        ax=fig.add_subplot(111, label="1")
        ax2=fig.add_subplot(111, label="2", frame_on=False)

        ax.plot(x, epsilons, color="C0")
        ax.set_xlabel("Game", color="C0")
        ax.set_ylabel("Epsilon", color="C0")
        ax.tick_params(axis='x', colors="C0")
        ax.tick_params(axis='y', colors="C0")

        N = len(scores)
        running_avg = np.empty(N)
        for t in range(N):
            running_avg[t] = np.mean(scores[max(0, t-20):(t+1)])

        ax2.scatter(x, running_avg, color="C1")
        #ax2.xaxis.tick_top()
        ax2.axes.get_xaxis().set_visible(False)
        ax2.yaxis.tick_right()
        #ax2.set_xlabel('x label 2', color="C1")
        ax2.set_ylabel('Score', color="C1")
        #ax2.xaxis.set_label_position('top')
        ax2.yaxis.set_label_position('right')
        #ax2.tick_params(axis='x', colors="C1")
        ax2.tick_params(axis='y', colors="C1")

        if lines is not None:
            for line in lines:
                plt.axvline(x=line)

        plt.savefig(filename)
    
    """Count number of zombies remained under current observation"""
    def _count_num_of_zombies(self):
        count = 0
        if u'entities' in self.ob:
            entities = self.ob["entities"]
            for e in entities:
                if e["name"] == "Zombie":
                    count += 1
        return count
    
    def run_dqn(self):
        for i in range(1,self.n_games+1):
            self.agent.tensorboard.step = i
            self._start_mission()
            score = 0
            done = False
            self.ob = None
            self.num_heals = 2
            while self.world_state.is_mission_running:
                current_reward = 0
                # initialize rewards/penalties
                self.move_backwards_reward = 0
                self.life_decrease_penalty = 0
                self.time_rewards = 0
                self.heal_rewards = 0
                self.world_state = self.agent_host.getWorldState()
                if self.world_state.number_of_observations_since_last_state > 0: 
                    # get observation
                    msg = self.world_state.observations[-1].text
                    self.ob = json.loads(msg)

                    # Check if life is dropped
                    if "Life" in self.ob:
                        life = self.ob[u'Life']
                        if life < self.current_life:
                            print("aaaaaaaaaaargh!!")
                            self.life_decrease_penalty += life - self.current_life # life decrease penalty
                            self.flash = True
                        self.current_life = life
                        
                        
                    self._get_position_and_orientation()
                    difference = self._calculate_turning_difference_from_zombies()
                    
                    # agent chooses action
                    ob_array = self._observation_to_array(self.ob)
                    #print(f'prev_ob: {ob_array}')
                    action = self.agent.choose_action(ob_array)
                    print("action",action)
                    self._translate_actions(action, difference)
                    
                    time.sleep(0.1)
                    
                
                    #keras calculations 
                    observation_ = self._get_next_observation()
                    self._check_num_zombies()
                    new_ob_array  = self._observation_to_array(observation_)
                    # print(f'next_ob: {new_ob_array}')
                    current_reward += self._get_current_rewards(current_reward)
                    score += current_reward
                    #self.visual.drawStats(score, self._count_num_of_zombies(), i)
                    self.agent.remember(ob_array, action, current_reward, new_ob_array, done)
                    self.agent.learn(done)
                    # Visualization
                    self.visual.drawMobs(self.ob['entities'], self.flash,score,self._count_num_of_zombies(),i)
                    self.flash = False
                    self._check_all_zombies_dead()
                
                elif self.all_zombies_dead == True:
                    self.all_zombies_dead = False
        
            
            self.eps_history.append(self.agent.epsilon)
            self.scores.append(score)

            avg_score = np.mean(self.scores[max(0, i-100):(i+1)])
            print('episode ', i+1, 'score %.2f' % score, 'average score %.2f' % avg_score)

            if not i % self.aggregate_episode_every or i == 1:
                self.agent.tensorboard.update_stats(reward_avg=avg_score, 
                reward_min=np.min(self.scores[max(0, i-100):(i+1)]), 
                reward_max=np.max(self.scores[max(0, i-100):(i+1)]), 
                epsilon=self.agent.epsilon)
                print(f"TensorBoard logdir: {self.agent.log_dir}")

            if i%10 == 0 and i > 0:
                self.agent.save_model()
                print('Saved Model :D')
                
        self._plot_dqn_results(self.scores, self.eps_history)

    def _act(self, world_state, agent_host, current_r ):
        """take 1 action in response to the current world state"""
        
        obs_text = world_state.observations[-1].text
        self.ob = json.loads(obs_text) # most recent observation
        #self._assign_observation()
        
        self.logger.debug(self.ob)
        if not u'XPos' in self.ob or not u'ZPos' in self.ob:
            self.logger.error("Incomplete observation received")
            return 0
        current_s = "%d:%d" % (int(self.ob[u'XPos']), int(self.ob[u'ZPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(self.ob[u'XPos']), float(self.ob[u'ZPos'])))
        if current_s not in self.Qtb:
            self.Qtb[current_s] = ([0] * self.n_actions)

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self._updateQTable( current_r, current_s )


        # select the next action
        rnd = random.random()
        if rnd < self.epsilon:
            action = random.randint(0, self.n_actions - 1)
        else:
            m = max(self.Qtb[current_s])
            self.logger.debug("Current values: %s" % ",".join(str(x) for x in self.Qtb[current_s]))
            l = list()
            for x in range(0, self.n_actions):
                if self.Qtb[current_s][x] == m:
                    l.append(x)
            y = random.randint(0, len(l)-1)
            action = l[y]
        

        # try to send the selected action, only update prev_s if this succeeds
        try:
            difference = self._calculate_turning_difference_from_zombies()
            self._translate_actions(action, difference)
            self.prev_s = current_s
            self.prev_a = action

        except RuntimeError as e:
            self.logger.error("Failed to send command: %s" % e)

        return current_r

    def run_qlearning(self):
        
        cumulative_rewards = []

        for i in range(self.n_games):
            self._start_mission()

            total_reward = 0
            is_first_action = True
            self.prev_s = None
            self.prev_a = None
            while self.world_state.is_mission_running:
                current_r = 0

                if is_first_action:
                    while True:
                        time.sleep(0.1)
                        self.world_state = self.agent_host.getWorldState()
                        for error in self.world_state.errors:
                            self.logger.error("Error: %s" % error.text)
                        for reward in self.world_state.rewards:
                            current_r += reward.getValue()
                        if self.world_state.is_mission_running and len(self.world_state.observations)>0 and not self.world_state.observations[-1].text=="{}":
                            total_reward += self._act(self.world_state, self.agent_host, current_r)
                            break
                        if not self.world_state.is_mission_running:
                            break
                    is_first_action = False
                    print(f"current reward = {current_r}")
                else:
                    # wait for non-zero reward
                    while self.world_state.is_mission_running and current_r == 0:
                        time.sleep(0.1)
                        self.world_state = self.agent_host.getWorldState()
                        for error in self.world_state.errors:
                            self.logger.error("Error: %s" % error.text)
                        for reward in self.world_state.rewards:
                            current_r += reward.getValue()
                        #print("waiting to stabilize")
                    # allow time to stabilise after action
                    while True:
                        time.sleep(0.1)
                        self.world_state = self.agent_host.getWorldState()
                        for error in self.world_state.errors:
                            self.logger.error("Error: %s" % error.text)
                        for reward in self.world_state.rewards:
                            current_r += reward.getValue()
                        if self.world_state.is_mission_running and len(self.world_state.observations)>0 and not self.world_state.observations[-1].text=="{}":
                            total_reward += self._act(self.world_state, self.agent_host, current_r)
                            break
                        if not self.world_state.is_mission_running:
                            break
                
                self._check_all_zombies_dead()
            

            # process final reward
            self.logger.debug("Final reward: %d" % current_r)
            print('Cumulative reward: %d' % total_reward)
            total_reward += current_r

            # update Q values
            if self.prev_s is not None and self.prev_a is not None:
                self._updateQTableFromTerminatingState( current_r )
                
            self._exportQTable() # export the Q table after each iteration
            cumulative_rewards += [ total_reward ]
            print("Cumulative rewards for all %d runs:" % self.n_games)
            print(cumulative_rewards)