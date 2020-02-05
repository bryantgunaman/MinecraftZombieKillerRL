from __future__ import print_function


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

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

# Task parameters:
ARENA_WIDTH = 10
ARENA_BREADTH = 10

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

mission_file = './zombie_killer.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
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
current_yaw = 0


# Loop until mission ends:
while world_state.is_mission_running:
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        print(f"OBSERVATIONS: {ob}")
        # Use the line-of-sight observation to determine when to hit and when not to hit:
        if 'LineOfSight' in ob:
            los = ob[u'LineOfSight']
            type=los["type"]
            if type == "Zombie":
                print("ATTACKING")
                agent_host.sendCommand("attack 1")
                agent_host.sendCommand("attack 0")
        # Get our position/orientation:
        if 'Yaw' in ob:
            current_yaw = ob[u'Yaw']
        if 'XPos' in ob:
            self_x = ob[u'XPos']
        if 'ZPos' in ob:
            self_z = ob[u'ZPos']
        # Use the nearby-entities observation to decide which way to move, and to keep track
        # of population sizes - allows us some measure of "progress".
        if 'entities' in ob:
            print('entities in ob')
            entities = ob["entities"]
            num_zombie = 0
            x_pull = 0
            z_pull = 0
            for e in entities:
                if e["name"] == "Zombie":
                    num_zombie += 1
                    # Each sheep contributes to the direction we should head in...
                    dist = max(0.0001, (e["x"] - self_x) * (e["x"] - self_x) + (e["z"] - self_z) * (e["z"] - self_z))
                    # Prioritise going after wounded sheep. Max zombie health is 21, according to Minecraft wiki...
                    weight = 21.0 - e["life"]
                    x_pull += weight * (e["x"] - self_x) / dist
                    z_pull += weight * (e["z"] - self_z) / dist
            # Determine the direction we need to turn in order to head towards the "sheepiest" point:
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

    # mission has ended.
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_rewards_since_last_state > 0:
        # A reward signal has come in - see what it is:
        total_reward += world_state.rewards[-1].getValue()

    print("Total score this round:", total_reward)
    print("=" * 41)
    print()
    time.sleep(1) # Give the mod a little time to prepare for the next mission.
    # break # Exits after one loop on purpose

for error in world_state.errors:
    print("Error:",error.text)

print()
print("Mission ended")

# Mission has ended.
