from __future__ import print_function
import malmo.minecraftbootstrap; malmo.minecraftbootstrap.set_malmo_xsd_path()
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


class MainKeras():

    def __init__(self, missionXML, n_games=500, max_retries=3):
        # keras attributes
        self.n_games = n_games
        self.agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.0005, input_dims=5,
                  n_actions=3, mem_size=1000000, batch_size=64, epsilon_end=0.01)
        self.scores = []
        self.eps_history = []

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
        self.my_mission = MalmoPython.MissionSpec(self.missionXML, True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        self.max_retries = max_retries

        #adding clients
        self.my_client_pool = None
        self._add_starters()
        self._add_default_client()

        
        self.world_state = None
        

        # main loop variables
        self.self_x = 0
        self.self_z = 0
        self.current_yaw = 0
        self.ob = None


    def _add_starters(self):
        self.my_mission.removeAllCommandHandlers()
        self.my_mission.allowAllDiscreteMovementCommands()
        #self.my_mission.requestVideo( 320, 240 )  use default size instead
        self.my_mission.setViewpoint( 0 )

    def _add_default_client(self):
        self.my_client_pool = MalmoPython.ClientPool()
        self.my_client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))

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

    def _calculate_turning_difference_from_zombies(self, ):
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
        return current_rewards

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


    def _translate_actions(self, action_num, difference_from_zombie):
        if action_num == 0:
            self._move_towards_zombies(difference_from_zombie)
        elif action_num ==1:
            self._move_away_from_zombies(difference_from_zombie)
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

    def _decrease_life_penalty(self):
        if len(self.world_state.observations) >= 2 and self.world_state.number_of_observations_since_last_state > 0:
            ob = json.loads(self.world_state.observations[-1].text)
            ob2 = json.loads(self.world_state.observations[-2].text)
            if ob2['Life'] < ob['Life']:
                return ob2['Life'] - ob['Life'] * 5
        return 0


    def run(self):
        for i in range(self.n_games):
            self._retry_start_mission()
            score = 0
            done = False
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
                    print(ob_array)
                    action = self.agent.choose_action(ob_array)
                    self._translate_actions(action, difference)
                    
                    #keras calculations
                    observation_ = self._get_next_observation()
                    new_ob_array  = self._basic_observation_to_array(observation_)
                    current_reward += self._get_current_rewards(current_reward)
                    score += current_reward
                    self.agent.remember(ob_array, action, current_reward, new_ob_array, done)
                    self.agent.learn()
                    

            self.eps_history.append(self.agent.epsilon)
            self.scores.append(score)

            avg_score = np.mean(self.scores[max(0, i-100):(i+1)])
            print('episode ', 1, 'score %.2f' % score, 'average score %.2f' % avg_score)

            if i%10 == 0 and i > 0:
                agent.save_model()
            
        # Plotting functions to be implemented later
        # filename = 'zombie_kill.png'
        # x = [i+1 for i in range(n_games)]
        #plotLearning(x, scores, eps_history, filename)






    





if __name__ == '__main__':
    with open('zombie_kill_1.xml', 'r') as file:
        mission_file = file.read().replace('\n', '')
        mk = MainKeras(mission_file, n_games=25, max_retries=3)
        mk.run()



    
    

    


