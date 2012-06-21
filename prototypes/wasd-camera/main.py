from pandac.PandaModules import * 
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task 



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
		


############################
#     mouselook class      #
############################
class mouselook(DirectObject):

	def __init__(self, camera):
		self.camera  = camera 
		self.running = False 
		self.time    = 0 
		self.centX   = base.win.getProperties().getXSize()/2 
		self.centY   = base.win.getProperties().getYSize()/2 

		# key controls 
		self.forward   = False 
		self.backward  = False 
		self.left      = False 
		self.right     = False 
		self.up        = False 
		self.down      = False 
		self.up        = False 
		self.down      = False 
		self.rollLeft  = False 
		self.rollRight = False 

		# sensitivity settings 
		self.movSens  = 2 
		self.rollSens = 50 
		self.sensX = self.sensY = 0.2          

	# camera rotation task 
	def cameraTask(task): 
		dt = task.time - self.time 

		# handle mouse look 
		md = base.win.getPointer(0)        
		x = md.getX() 
		y = md.getY() 

		if base.win.movePointer(0, self.centX, self.centY):    
			self.camera.setH(self.camera,self.camera.getH(self.camera) - (x - self.centX) * self.sensX) 
			self.camera.setP(self.camera,self.camera.getP(self.camera) - (y - self.centY) * self.sensY)       

		# handle keys: 

		if self.forward == True: 
			self.camera.setY(self.camera, self.camera.getY(self.camera) + self.movSens*dt) 
		if self.backward == True: 
			self.camera.setY(self.camera, self.camera.getY(self.camera) - self.movSens*dt) 
		if self.left == True: 
			self.camera.setX(self.camera, self.camera.getX(self.camera) - self.movSens*dt) 
		if self.right == True: 
			self.camera.setX(self.camera, self.camera.getX(self.camera) + self.movSens*dt) 
		if self.up == True: 
			self.camera.setZ(self.camera, self.camera.getZ(self.camera) + self.movSens*dt) 
		if self.down == True: 
			self.camera.setZ(self.camera, self.camera.getZ(self.camera) - self.movSens*dt)           
		if self.rollLeft == True: 
			self.camera.setR(self.camera, self.camera.getR(self.camera) - self.rollSens*dt) 
		if self.rollRight == True: 
			self.camera.setR(self.camera, self.camera.getR(self.camera) + self.rollSens*dt) 

		self.time = task.time       
		return task.cont 

	def start(self):   
		base.disableMouse() 
		# hide mouse cursor, comment these 3 lines to see the cursor 
		props = WindowProperties() 
		props.setCursorHidden(True) 
		base.win.requestProperties(props) 
		# reset mouse to start position: 
		base.win.movePointer(0, self.centX, self.centY)             
		taskMgr.add(self.cameraTask, 'HxMouseLook::cameraTask') 

		
#######################################
#  objects of class mouselook & WASD  #
#######################################

mouse_look = mouselook()
mouse_look.start()
wasd_control = wasdControl()

####################
# runs the program #
####################

run()
