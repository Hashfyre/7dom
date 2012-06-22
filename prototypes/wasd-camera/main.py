from pandac.PandaModules import * 
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject




################
# housekeeping #
################

# import stage model and make it render
stage = loader.loadModel("models/environment")
stage.reparentTo(render)

# disable the default mouse-controls for the camera
base.disableMouse()


#################
# WASD movement #
#################

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

####################
# runs the program #
####################

run()
