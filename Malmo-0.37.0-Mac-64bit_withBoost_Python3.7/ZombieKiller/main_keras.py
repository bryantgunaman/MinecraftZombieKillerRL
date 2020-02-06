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
        agent_host = MalmoPython.AgentHost()

        try:
            agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(agent_host.getUsage())
            exit(1)
        if agent_host.receivedArgument("help"):
            print(agent_host.getUsage())
            exit(0)

        print(missionXML)
        self.my_mission = MalmoPython.MissionSpec(missionXML, True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        self.max_retries = max_retries

        self._add_starters()
        self._add_default_client()

    def _add_starters(self):
        my_mission.removeAllCommandHandlers()
        my_mission.allowAllDiscreteMovementCommands()
        my_mission.requestVideo( 320, 240 )
        my_mission.setViewpoint( 1 )

    def _add_default_client(self):
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000))



    # def run(self):
    #     for i in range(self.n_games):
    #         while 




if __name__ == '__main__':
    with open('default_flat_1.xml', 'r') as file:
        mission_file = file.read().replace('\n', '')
        # print(data)

        mk = MainKeras(mission_file, n_games=500, max_retries=3)



    
    

    


