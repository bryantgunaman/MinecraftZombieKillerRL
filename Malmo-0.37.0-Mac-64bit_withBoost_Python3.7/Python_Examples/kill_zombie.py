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

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
import MalmoPython
import os
import sys
import time
import json
import math

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
                  <ContinuousMovementCommands turnSpeedDegs="360"/>
                  <ObservationFromRay/>
                  <RewardForDamagingEntity>
                    <Mob type="Zombie" reward="1"/>
                  </RewardForDamagingEntity>
                  <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                  </ObservationFromNearbyEntities>
                  <ObservationFromFullStats/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

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

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

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
print("Mission running ", end=' ')

# main loop:
total_reward = 0
zombie_population = 0
self_x = 0
self_z = 0
current_yaw = 30

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        print(f"OBSERVATIONS: {ob}")
        # Use the line-of-sight observation to determine when to hit and when not to hit:
        if u'LineOfSight' in ob:
            print('LINE OF SIGHT\n',ob[u'LineOfSight'])
            los = ob[u'LineOfSight']
            type=los["type"]
            if type == "Zombie":
                print("ATTACKING")
                agent_host.sendCommand("attack 1")
                agent_host.sendCommand("attack 0")
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
                    num_pigs += 1
            # Determine the direction we need to turn in order to head towards the "zombiest" point:
            yaw = -180 * math.atan2(x_pull, z_pull) / math.pi
            difference = yaw - current_yaw;
            while difference < -180:
                difference += 360;
            while difference > 180:
                difference -= 360;
            difference /= 180.0;
            print('TURNING')
            agent_host.sendCommand("turn " + str(difference))
            move_speed = 1.0 if abs(difference) < 0.5 else 0  # move slower when turning faster - helps with "orbiting" problem
            print('MOVING')
            agent_host.sendCommand("move " + str(move_speed))
            if num_zombie != zombie_population:
                # Print an update of our "progress":
                zombie_population = num_zombie
                if zombie_population:
                    print(f'zombie_population: {zombie_population}')

        if world_state.number_of_rewards_since_last_state > 0:
            # Keep track of our total reward:
            total_reward += world_state.rewards[-1].getValue()
    # mission has ended
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_rewards_since_last_state > 0:
        # A reward signal has come in - see what it is:
        total_reward += world_state.rewards[-1].getValue()

    print("Total score this round:", total_reward)
    print("=" * 41)
    print()
    time.sleep(1) # Give the mod a little time to prepare for the next mission.
print("Mission ended")
# Mission has ended.
