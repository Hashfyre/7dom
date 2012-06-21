import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from MouseControls import * 
from direct.task import Task 



################
# housekeeping #
################

# import stage model and make it render
stage = loader.loadModel("models/environment")
stage.reparentTo(render)

# disable the default mouse-controls for the camera
base.disableMouse()


###############
# actual code #
###############

class wasdControl(DirectObject):
	
	def __init__(self):
		self.accept('w-repeat', self.forward, [globalClock.getDt()])
		self.accept('s-repeat', self.backward, [globalClock.getDt()])
		self.accept('a-repeat', self.leftward, [globalClock.getDt()])
		self.accept('d-repeat', self.rightward, [globalClock.getDt()])
	
	def forward(self, dt):
		camera.setY(camera.getY()+1*dt)
		
	def backward(self, dt):
		camera.setY(camera.getY()-0.7*dt)
		
	def leftward(self, dt):
		camera.setX(camera.getX()-0.8*dt)
		
	def rightward(self, dt):
		camera.setX(camera.getX()+0.8*dt)
		
	def squidward(self, dt):
		print "It's 'Mr. Tentacles' for you!"
		
wasd_control = wasdControl()

############################
#     mouselook class      #
############################

class hlview(DirectObject): 

    def __init__(self): 
        self.m=MouseControls() 
        base.enableMouse() 
        
    def start(self): 
        self.m.startMouse() 
        base.disableMouse() 
        par=camera.getParent() 
        self.parent=par 
        #Our base node that only holds position 
        self.posNode=par.attachNewNode("PosNode") 
        self.posNode.setPos(camera.getPos(par)) 

        #Orient the camera on the posNode 
        camera.setPos(0,0,0) 
        camera.reparentTo(self.posNode) 
        
        #Task for changing direction/position 
        taskMgr.add(self.camTask, "hlview::camTask")           
    
    def camTask(self,task): 
        #position change 
        finalMove=Vec3(0,0,0) 
        basePosition=self.posNode.getPos(self.parent) 
        self.posNode.setPos(self.posNode.getPos()+finalMove) 
        x=-self.m.mouseChangeX*.2 
        y=-self.m.mouseChangeY*.1 
        #orientation change 
        camera.setH(camera.getH()+x) 
        camera.setP(camera.getP()+y) 
        return Task.cont 
		
############################
#  object of class hlview  #
############################
  
import hlview 
mouseControl=hlview.hlview() 
mouseControl.start() 

####################
# runs the program #
####################

run()
