from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

from builtins import range
import MalmoPython
import os
import random
import sys
import time
import json
import logging
import math
import json

if sys.version_info[0] == 2:
    # Workaround for https://github.com/PythonCharmers/python-future/issues/262
    import Tkinter as tk
else:
    import tkinter as tk

QTable_file = 'QTable.txt' # Global variable for potential saved Q table

class TabQAgent(object):
    """Tabular Q-learning agent for discrete state/action spaces."""

    def __init__(self):
        self.epsilon = 0.01 # chance of taking a random action instead of the best

        self.logger = logging.getLogger(__name__)
        if False: # True if you want to see more information
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.actions = ["towards_zombies", "away_from_zombies", "attack once"] # All possible actions
        if QTable_file == None:
            self.q_table = {}
        else:
            with open('QTable.txt') as json_file:
                Qtb = json.load(json_file)
            self.q_table = Qtb
        self.canvas = None
        self.root = None
        self.num_zombie = 0
        self.zombie_population = 0
    
    def exportQTable(self):
        with open('QTable.txt', 'w') as outfile:
            json.dump(self.q_table, outfile)

    def calculate_turning_difference(self,agent_host):
        """ calculate turning difference based on where zombies are """
        world_state = agent_host.getWorldState()
        difference = 0
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            print(f"OBSERVATIONS: {ob}")
            # Get our position/orientation:
            if u'Yaw' in ob:
                current_yaw = ob[u'Yaw']
            if u'XPos' in ob:
                self_x = ob[u'XPos']
            if u'ZPos' in ob:
                self_z = ob[u'ZPos']
            # Use the nearby-entities observation to decide which way to move, and to keep track
            # of population sizes - allows us some measure of "progress".
            if u'entities' in ob:
                print('entities in ob')
                entities = ob["entities"]
                num_zombie = 0
                x_pull = 0
                z_pull = 0
                for e in entities:
                    if e["name"] == "Zombie":
                        num_zombie += 1
                        # Each zombie contributes to the direction we should head in...
                        dist = max(0.0001, (e["x"] - self_x) * (e["x"] - self_x) + (e["z"] - self_z) * (e["z"] - self_z))
                        # Prioritise going after wounded sheep. Max zombie health is 20, according to Minecraft wiki...
                        weight = 21.0 - e["life"]
                        x_pull += weight * (e["x"] - self_x) / dist
                        z_pull += weight * (e["z"] - self_z) / dist
                    elif e["name"] == "Zombie":
                        num_zombie += 1
            # Determine the direction we need to turn in order to head towards the "zombiest" point:
            yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
            difference = yaw - current_yaw
            while difference < -180:
                difference += 360
            while difference > 180:
                difference -= 360
            difference /= 180.0
        print("turn differece: ", difference)
        return difference

    def send_command(self,agent_host, a):
        """ based on random integer a and the observation send customized actions"""
        if a == 0: # case "towards_zombies"
            difference = self.calculate_turning_difference(agent_host)
            print('TURNING')
            agent_host.sendCommand("turn " + str(difference))
            move_speed = 1.0 if abs(difference) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
            print('MOVING')
            agent_host.sendCommand("move " + str(move_speed))
            if self.num_zombie != self.zombie_population:
                # Print an update of our "progress":
                self.zombie_population = self.num_zombie
                if self.zombie_population:
                    print(f'self.zombie_population: {self.zombie_population}')
        elif a == 1:
            difference = self.calculate_turning_difference(agent_host)
            print('TURNING')
            agent_host.sendCommand("turn " + str(difference))
            move_speed = 1.0 if abs(difference) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
            print('MOVING')
            agent_host.sendCommand("move -" + str(move_speed)) # moving backwards
            if self.num_zombie != self.zombie_population:
                # Print an update of our "progress":
                self.zombie_population = self.num_zombie
                if self.zombie_population:
                    print(f'self.zombie_population: {self.zombie_population}')
        else:
            agent_host.sendCommand("attack 1")
            agent_host.sendCommand("attack 0")
            
    def updateQTable( self, reward, current_state ):
        """Change q_table to reflect what we have learnt."""
        
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.q_table[self.prev_s][self.prev_a]
        
        # TODO: what should the new action value be?
        new_q = reward
        
        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q
        
    def updateQTableFromTerminatingState( self, reward ):
        """Change q_table to reflect what we have learnt, after reaching a terminal state."""
        
        # retrieve the old action value from the Q-table (indexed by the previous state and the previous action)
        old_q = self.q_table[self.prev_s][self.prev_a]
        
        # TODO: what should the new action value be?
        new_q = reward
        
        # assign the new action value to the Q-table
        self.q_table[self.prev_s][self.prev_a] = new_q
        
    def act(self, world_state, agent_host, current_r ):
        """take 1 action in response to the current world state"""
        
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text) # most recent observation
        self.logger.debug(obs)
        if not u'XPos' in obs or not u'ZPos' in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0
        current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))
        if current_s not in self.q_table:
            self.q_table[current_s] = ([0] * len(self.actions))

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTable( current_r, current_s )


        # select the next action
        rnd = random.random()
        if rnd < self.epsilon:
            a = random.randint(0, len(self.actions) - 1)
            self.logger.info("Random action: %s" % self.actions[a])
        else:
            m = max(self.q_table[current_s])
            self.logger.debug("Current values: %s" % ",".join(str(x) for x in self.q_table[current_s]))
            l = list()
            for x in range(0, len(self.actions)):
                if self.q_table[current_s][x] == m:
                    l.append(x)
            y = random.randint(0, len(l)-1)
            a = l[y]
            self.logger.info("Taking q action: %s" % self.actions[a])

        # try to send the selected action, only update prev_s if this succeeds
        try:
            self.send_command(agent_host,a)
            self.prev_s = current_s
            self.prev_a = a

        except RuntimeError as e:
            self.logger.error("Failed to send command: %s" % e)

        return current_r

    def run(self, agent_host):
        """run the agent on the world"""

        total_reward = 0
        
        self.prev_s = None
        self.prev_a = None
        
        is_first_action = True
        
        # main loop:
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:

            current_r = 0
            
            if is_first_action:
                # wait until have received a valid observation
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        break
                is_first_action = False
            else:
                # wait for non-zero reward
                while world_state.is_mission_running and current_r == 0:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                # allow time to stabilise after action
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations)>0 and not world_state.observations[-1].text=="{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        break

        # process final reward
        self.logger.debug("Final reward: %d" % current_r)
        total_reward += current_r

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTableFromTerminatingState( current_r )
            
        self.exportQTable() # export the Q table after each iteration
        return total_reward
########

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Task parameters:
ARENA_WIDTH = 20
ARENA_BREADTH = 20

missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            
              <About>
                <Summary>Hello world!</Summary>
              </About>
              
              <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>15000</StartTime>
                        <AllowPassageOfTime>true</AllowPassageOfTime>
                    </Time>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,2*3,2;1;"/>
                  <DrawingDecorator>
                    <DrawLine x1="2" y1="4" z1="-2" x2="2" y2="4" z2="8" type="fence"/>
                    <DrawLine x1="2" y1="4" z1="8" x2="-8" y2="4" z2="8" type="fence"/>
                    <DrawLine x1="-8" y1="4" z1="8" x2="-8" y2="4" z2="-2" type="fence"/>
                    <DrawLine x1="2" y1="4" z1="-2" x2="-8" y2="4" z2="-2" type="fence"/>
                    <DrawEntity x="-7" y="4" z="7" type="Zombie"/>
                  </DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="20000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>ZombieKiller</Name>
                <AgentStart>
                    <Placement x="0" y="4" z="0" yaw="30"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_sword"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <ObservationFromRecentCommands/>
                    <ContinuousMovementCommands turnSpeedDegs="420"/>
                    <ObservationFromRay/>
                    <RewardForDamagingEntity>
                        <Mob type="Zombie" reward="100"/>
                    </RewardForDamagingEntity>
                    <RewardForSendingCommand reward="-1" />
                    <ObservationFromNearbyEntities>
                        <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                    </ObservationFromNearbyEntities>
                    <ObservationFromFullStats/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Final state: no zombies -- big rewards
# Create default Malmo objects:
agent = TabQAgent()
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

# Attempt to start a mission:
my_mission = MalmoPython.MissionSpec(missionXML, True)
max_retries = 3
num_repeats = 10
cumulative_rewards = []
for i in range(num_repeats):
    print()
    print('Repeat %d of %d' % ( i+1, num_repeats))
    my_mission_record = MalmoPython.MissionRecordSpec()

    for retry in range(max_retries):
        try:
            my_mission.forceWorldReset() # force world to reset for each iteration
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:",e)
                exit(1)
            else:
                time.sleep(2.5)

    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)
    print()

    # -- run the agent in the world -- #
    cumulative_reward = agent.run(agent_host)
    print('Cumulative reward: %d' % cumulative_reward)
    cumulative_rewards += [ cumulative_reward ]

    # -- clean up -- #
    time.sleep(1) # (let the Mod reset)

print()
print("Cumulative rewards for all %d runs:" % num_repeats)
print(cumulative_rewards)
print("Mission ended")
# Mission has ended.
