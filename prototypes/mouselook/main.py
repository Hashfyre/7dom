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

# lets us quit with the escape key instead of the mouse (alt+f4 works too, of course)
base.accept("escape", quit) 
def quit():
    sys.exit
    print "should have quited" 



############################
#     mouselook class      #
############################
class Mouselook(DirectObject):

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
		#prev val 2
		self.movSens  = 0.1
		#prev val 50
		self.rollSens = 0 
		self.sensX = self.sensY = 0.1 
		
		print "okay"         
		taskMgr.add(self.cameraTask, 'cameraTask') 

	# camera rotation task 
	def cameraTask(self, task): 
		dt = task.time - self.time 

		# handle mouse look 
		md = base.win.getPointer(0)        
		x = md.getX() 
		y = md.getY()

		if base.win.movePointer(0, self.centX, self.centY):    
			self.camera.setH(self.camera,self.camera.getH(self.camera) - (x - self.centX) * self.sensX) 
			self.camera.setP(self.camera,self.camera.getP(self.camera) - (y - self.centY) * self.sensY)       

		# handle keys: 

		#if self.forward == True: 
		#	self.camera.setY(self.camera, self.camera.getY(self.camera) + self.movSens*dt) 
		#if self.backward == True: 
		#	self.camera.setY(self.camera, self.camera.getY(self.camera) - self.movSens*dt) 
		#if self.left == True: 
		#	self.camera.setX(self.camera, self.camera.getX(self.camera) - self.movSens*dt) 
		#if self.right == True: 
		#	self.camera.setX(self.camera, self.camera.getX(self.camera) + self.movSens*dt) 
		#if self.up == True: 
		#	self.camera.setZ(self.camera, self.camera.getZ(self.camera) + self.movSens*dt) 
		#if self.down == True: 
		#	self.camera.setZ(self.camera, self.camera.getZ(self.camera) - self.movSens*dt)           
		#if self.rollLeft == True: 
		#	self.camera.setR(self.camera, self.camera.getR(self.camera) - self.rollSens*dt) 
		#if self.rollRight == True: 
		#	self.camera.setR(self.camera, self.camera.getR(self.camera) + self.rollSens*dt) 

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

mouse_look = Mouselook(camera)
mouse_look.start()

####################
# runs the program #
####################

run()
