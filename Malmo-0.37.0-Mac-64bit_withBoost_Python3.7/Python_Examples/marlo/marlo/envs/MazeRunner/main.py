1#!/usr/bin/env python
import marlo
from marlo import MarloEnvBuilderBase
from marlo import MalmoPython


import os
from pathlib import Path


class MarloEnvBuilder(MarloEnvBuilderBase):
    """
    Description: 
		The layout of this map is that of a maze; the goal of the mission is to reach
		the redstone pillar at the end of the maze.
		
	Observations:
		A depth map is provided for the agent to use, which trivializes this task.
		
	Actions available:
		Jump
		Move
		Pitch
		Turn
		Crouch
		Attack
		Use
		
	Rewards:
		nil
    """
	
    def __init__(self, extra_params={}):
        super(MarloEnvBuilder, self).__init__(
                templates_folder = os.path.join(
                            str(Path(__file__).parent),
                            "templates"
                )
        )
        self.params = self._default_params()
        # You can do something with the extra_params if you wish
        self.params.update(extra_params)
        print(self.params["maze_height"])
        print(extra_params)

    def _default_params(self):
        _default_params = super(MarloEnvBuilder, self).default_base_params
        _default_params.update(
            dict(
                tick_length = 50,
                agent_names=["MarLo-agent0"],
                maze_height= 2
            )
        )
        return _default_params


if __name__ == "__main__":
    env_builder =  MarloEnvBuilder()
    print(env_builder.params)
    print(env_builder.params.experiment_id)
    mission_xml = env_builder.render_mission_spec()
    mission_spec = MalmoPython.MissionSpec(mission_xml, True)
    print(mission_spec.getSummary())
