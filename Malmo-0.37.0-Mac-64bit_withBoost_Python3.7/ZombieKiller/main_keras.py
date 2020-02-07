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
        self.n_games = n_games
        self.agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.0005, input_dims=8,
                  n_actions=4, mem_size=1000000, batch_size=64, epsilon_end=0.01)
        self.scores = []
        self.eps_history = []
        self.agent_host = MalmoPython.AgentHost()

        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(self.agent_host.getUsage())
            exit(1)
    
        print(missionXML)
        self.my_mission = MalmoPython.MissionSpec(missionXML, True)
        self.my_mission.setViewpoint(0)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        self.max_retries = max_retries

        #adding clients
        self.my_client_pool = None
        self._add_starters()
        self._add_default_client()

        # attempting to start the mission
        self.world_state = None
        self._retry_start_mission()

        # main loop variables
        self.total_reward = 0
        self.pig_population = 0
        self.sheep_population = 0
        self.self_x = 0
        self.self_z = 0
        self.current_yaw = 0


    def _add_starters(self):
        self.my_mission.removeAllCommandHandlers()
        self.my_mission.allowAllDiscreteMovementCommands()
        self.my_mission.requestVideo( 320, 240 )
        self.my_mission.setViewpoint( 1 )

    def _add_default_client(self):
        self.my_client_pool = MalmoPython.ClientPool()
        self.my_client_pool.add(MalmoPython.ClientInfo('127.0.0.1', 10000))

    def _retry_start_mission(self):
        self.my_mission_record = MalmoPython.MissionRecordSpec()
        
        for retry in range(self.max_retries):
            try:
                # Attempt to start the mission:
                self.agent_host.startMission( self.my_mission, self.my_client_pool, 
                self.my_mission_record, 0, "ZombieKiller" )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
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


    # def run(self):
    #     for i in range(self.n_games):
    #         while 




if __name__ == '__main__':
    with open('zombie_kill_1.xml', 'r') as file:
        mission_file = file.read().replace('\n', '')
        mk = MainKeras(mission_file, n_games=500, max_retries=3)



    
    

    


