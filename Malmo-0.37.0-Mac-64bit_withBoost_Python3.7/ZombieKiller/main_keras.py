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
import matplotlib.pyplot as plt

class MainKeras():

    def __init__(self, missionXML, n_games=500, max_retries=3, starting_zombies=1,
                 XSize=10, ZSize=10, load_model=False):
        # keras attributes
        self.n_games = n_games

        self._init_logger()

        # keras
        self.n_actions = 3
        self.agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.0005, input_dims=5,
                  n_actions=3, mem_size=1000000, batch_size=64, epsilon_end=0.01)
        self._load_dqn_model(load_model)

        self.scores = []
        self.eps_history = []

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
        
        #mission generator
        self.mission_generator = MissionGenerator(self.missionXML)
        self.starting_zombies = starting_zombies
        self.XSize = XSize
        self.ZSize = ZSize

        # main loop variables
        self.self_x = 0
        self.self_z = 0
        self.current_yaw = 0
        self.ob = None

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

    def _add_starters(self):
        # self.my_mission.removeAllCommandHandlers()
        self.my_mission.allowAllContinuousMovementCommands()
        self.my_mission.setViewpoint( 0 )
        # self.my_mission.allowAllDiscreteMovementCommands()
        #self.my_mission.requestVideo( 320, 240 )  use default size instead
    
    def _validate_mission(self):
        self.my_mission = MalmoPython.MissionSpec(self.mission_generator.getXML(), True)
        # self.my_mission_record = MalmoPython.MissionRecordSpec()
    
    def _drawBoundaries(self):
        for i in range(len(self.xcoords)):
            self.my_mission.drawLine(self.xcoords[i % len(self.xcoords)] , 4, self.zcoords[i % len(self.xcoords)], self.xcoords[(i+1) % len(self.xcoords)], 4, self.zcoords[(i+1) % len(self.xcoords)], "fence")


    def _retry_start_mission(self):
        self.my_mission_record = MalmoPython.MissionRecordSpec()
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
        self.world_state = self.agent_host.getWorldState()
        while not self.world_state.has_mission_begun:
            time.sleep(0.1)
            self.world_state = self.agent_host.getWorldState()

    def _assign_observation(self):
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
            self.ob = json.loads(msg)

    def _get_next_observation(self):
        self.world_state = self.agent_host.getWorldState()
        if self.world_state.number_of_observations_since_last_state > 0:
            msg = self.world_state.observations[-1].text
            # while json.loads(msg) == self.ob:  # wait until the ob is different to get next
            #     pass
            return json.loads(msg)
        return self.ob
    
    def _get_position_and_orientation(self):
        if u'Yaw' in self.ob:
            self.current_yaw = self.ob[u'Yaw']
        if u'XPos' in self.ob:
            self.self_x = self.ob[u'XPos']
        if u'ZPos' in self.ob:
            self.self_z = self.ob[u'ZPos']

    def _get_turning_difference_from_zombies(self):
        diagonal_diff = self.get_diagonal_difference_from_zombies()
        if diagonal_diff != None:
            x_pull, z_pull = diagonal_diff

    def _calculate_turning_difference_from_zombies(self):
        x_pull, z_pull = self._get_diagonal_difference_from_zombies()
        yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
        difference = yaw - self.current_yaw
        while difference < -180:
            difference += 360
        while difference > 180:
            difference -= 360
        return difference / 180.0
        
    def _get_diagonal_difference_from_zombies(self):
        if u'entities' in self.ob:
            entities = self.ob["entities"]
            # print(f'Entities: {entities}')
            return self._get_pull_from_entities(entities) 
    
    def _get_pull_from_entities(self, entities):
        num_zombie, x_pull, z_pull = 0, 0, 0
        for e in entities:
            if e["name"] == "Zombie":
                num_zombie += 1
                # Each zombie contributes to the direction we should head in...
                dist = max(0.0001, (e["x"] - self.self_x) * (e["x"] - self.self_x) + (e["z"] - self.self_z) * (e["z"] - self.self_z))
                # Prioritize going after wounded zombie. Max zombie health is 20, according to Minecraft wiki...
                weight = 21.0 - e["life"]
                x_pull += weight * (e["x"] - self.self_x) / dist
                z_pull += weight * (e["z"] - self.self_z) / dist
            elif e["name"] == "Zombie":
                num_zombie += 1
        return x_pull, z_pull

    def _get_current_rewards(self, current_rewards):
        for reward in self.world_state.rewards:
            current_rewards += reward.getValue()
        current_rewards += self._decrease_life_penalty()
        current_rewards += self._increase_time_penalty()
        return current_rewards

    def _decrease_life_penalty(self):
        if len(self.world_state.observations) >= 2 and self.world_state.number_of_observations_since_last_state > 0:
            ob = json.loads(self.world_state.observations[-1].text)
            ob2 = json.loads(self.world_state.observations[-2].text)
            if ob2['Life'] < ob['Life']:
                return ob2['Life'] - ob['Life'] * 5
        return 0

    def _increase_time_penalty(self):
        if len(self.world_state.observations) >= 2 and self.world_state.number_of_observations_since_last_state > 0:
            ob = json.loads(self.world_state.observations[-1].text)
            ob2 = json.loads(self.world_state.observations[-2].text)
            if ob2['TimeAlive'] > ob['TimeAlive']:
                return ob['TimeAlive'] - ob2['TimeAlive'] * 2
        return 0

    def _move_towards_zombies(self, difference_from_zombie):
        self.agent_host.sendCommand("turn " + str(difference_from_zombie))
        move_speed = 1.0 if abs(difference_from_zombie) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
        self.agent_host.sendCommand("move " + str(move_speed))
        print("move " + str(move_speed))

    def _move_away_from_zombies(self, difference_from_zombie):
        self.agent_host.sendCommand("turn " + str(difference_from_zombie))
        move_speed = 1.0 if abs(difference_from_zombie) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
        self.agent_host.sendCommand("move -" + str(move_speed))
        print("move -" + str(move_speed))

    def _attack(self):
        self.agent_host.sendCommand("attack 1")
        self.agent_host.sendCommand("attack 0")
        print('attack')

    def _translate_actions(self, action_num, difference_from_zombie):
        if action_num == 0:
            self._move_away_from_zombies(difference_from_zombie)  
        elif action_num ==1:
            self._move_towards_zombies(difference_from_zombie)
        elif action_num == 2:
            self._attack()    
    
    def _basic_observation_to_array(self, ob):
        obs_array = []
        obs_array.append(ob['TimeAlive']) if 'TimeAlive' in ob else 0
        obs_array.append(ob['Life']) if 'Life' in ob else 0
        obs_array.append(ob['XPos']) if 'XPos' in ob else 0
        obs_array.append(ob['YPos']) if 'YPos' in ob else 0
        obs_array.append(ob['ZPos']) if 'ZPos' in ob else 0
        return np.array(obs_array)

    def _observation_to_array(self, observation):
        pass

    def _parse_entities(self, entities):
        pass

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
            self.agent_host.sendCommand("quit")

    def _plot_dqn_results(self, scores, eps_history, filename='zombie_kill.png', lines=None):
        x = [i+1 for i in range(self.n_games)]
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


    def run_dqn(self):
        for i in range(self.n_games):
            self._start_mission()
            score = 0
            done = False
            print(f'Iteration Number: {i}')
            while self.world_state.is_mission_running:
                current_reward = 0
                self.world_state = self.agent_host.getWorldState()
                self._assign_observation()
                if self.ob != None:
                    self._get_position_and_orientation()
                    difference = self._calculate_turning_difference_from_zombies()
                    # self.ob['difference'] = difference # add this later as state maybe

                    # agent chooses action
                    ob_array = self._basic_observation_to_array(self.ob)
                    print(f'prev_ob: {ob_array}')
                    action = self.agent.choose_action(ob_array)
                    self._translate_actions(action, difference)

                    #keras calculations
                    observation_ = self._get_next_observation()
                    new_ob_array  = self._basic_observation_to_array(observation_)
                    print(f'next_ob: {new_ob_array }')
                    current_reward += self._get_current_rewards(current_reward)
                    score += current_reward
                    self.agent.remember(ob_array, action, current_reward, new_ob_array, done)
                    self.agent.learn()

                    self._check_all_zombies_dead()
                            
                    
            self.eps_history.append(self.agent.epsilon)
            self.scores.append(score)

            avg_score = np.mean(self.scores[max(0, i-100):(i+1)])
            print('episode ', 1, 'score %.2f' % score, 'average score %.2f' % avg_score)

            if i%10 == 0 and i > 0:
                self.agent.save_model()
        
        self._plot_dqn_results(self.scores, self.eps_history)

    def _act(self, world_state, agent_host, current_r ):
        """take 1 action in response to the current world state"""
        
        # obs_text = world_state.observations[-1].text
        # obs = json.loads(obs_text) # most recent observation
        self._assign_observation()
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
                        print("waiting to stabilize")
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
            total_reward += current_r

            # update Q values
            if self.prev_s is not None and self.prev_a is not None:
                self._updateQTableFromTerminatingState( current_r )
                
            self._exportQTable() # export the Q table after each iteration
            cumulative_rewards += [ total_reward ]






    









    
    

    


