

class MissionGenerator():


    def __init__(self):
        
        # Task parameters:
        self._arena_width = 10
        self._arena_breadth = 10

        self._missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
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
                  <ServerQuitFromTimeUp timeLimitMs="120000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>
              
              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0" y="4" z="0" yaw="30"/>
                    <Inventory>
                        <InventoryItem slot="0" type="diamond_sword"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="420"/>
                <DiscreteMovementCommands> 

                    <ModifierList type="deny-list"> 
                        <command>attack</command> 
                        <command>turn</command> 
                        <command>move</command> 
                    </ModifierList> 
                </DiscreteMovementCommands> 
                <ContinuousMovementCommands> 
                    
                    <ModifierList type="allow-list">
                     <command>attack</command> 
                     
                    </ModifierList> 
                   
                </ContinuousMovementCommands>
          
                <ObservationFromRay/>
                 <RewardForDamagingEntity>
                    <Mob type="Zombie" reward="1"/>
                </RewardForDamagingEntity>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(self._arena_width)+'''" yrange="2" zrange="'''+str(self._arena_breadth)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


    def writeFile(self):
        file = f = open("zombie_kill_1.xml", "w")
        file.write(self._missionXML)
        file.close()


if __name__ == '__main__':
    mg = MissionGenerator()
    print('Starting.....')
    mg.writeFile()
    print('Finished')


