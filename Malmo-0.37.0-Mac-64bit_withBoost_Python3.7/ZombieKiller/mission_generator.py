from random import randrange
class MissionGenerator():
    def __init__(self, xml_file):
        
        # Task parameters:
        #default coordinates
        self._x = 10
        self._y = 4
        self._z = 10
        self._file = xml_file
        with open(self._file,'r') as f:
            self._initial_missionXML = f.read()
            self._missionXML = self._initial_missionXML
    
    # reverts self._missionXML to the original missionXML
    def restartXML(self):
        self._missionXML = self._initial_missionXML

    #adds DrawEntity into XML specified number of times
    def drawEntity(self, type, amount=1):
        for i in range(amount):
            #randomizes position of zombies
            x = randrange(2, self._x-1)
            z = randrange(2, self._z-1)
            
            draw_dec = '<DrawingDecorator>'
            draw_len = len(draw_dec)
            draw_ind = draw_len+self._missionXML.find(draw_dec)
            self._missionXML = self._missionXML[:draw_ind] + '\n\t\t\t<DrawEntity x="{}" y="{}" z="{}" type="{}"/>'.format(x,self._y,z,type) + self._missionXML[draw_ind:]

    #returns array of coordinates needed to create boundary
    def getCoords(self, x, z):
        self._x = x
        self._z = z
        xcoords = [0,0,x,x]
        zcoords = [0,z,z,0]
        return xcoords, zcoords
    
    #returns XML
    def getXML(self):
        return self._missionXML
    
    #randomizes spawn position of agent
    def randomStart(self):
        agent_start = '<AgentStart>'
        len_agent_start = len(agent_start)
        agent_ind = len_agent_start + self._missionXML.find(agent_start)
        self._missionXML = self._missionXML[:agent_ind] + '\n\t\t\t<Placement x="{}" y="{}" z="{}" yaw="{}"/>'.format(randrange(2,self._x-1), self._y, randrange(2,self._z-1), randrange(360)) + self._missionXML[agent_ind:]

    #writes XML into file
    def writeFile(self):
        file = f = open(self._file, "w")
        file.write(self._missionXML)
        file.close()