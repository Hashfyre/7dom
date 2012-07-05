from pandac.PandaModules import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.bullet import *

class Entity(DirectObject):
	
	def __init__(self, world, parent, shape=BulletCapsuleShape(0.5, 1), pos=(0, 0, 2)):
		"""Creates a generic Entity with a physical component.

		Keyword arguments:
		world 	-- a BulletWorld object to add the Entity's physical body to
		parent 	-- the Node under which the Entity's physical body will be added
		shape 	-- a BulletShape object for the Entity's physical body (default BulletCapsuleShape(0.5, 1))
		pos 	-- a three-tuple for the position of the Entity with respect of its parent (default (0, 0, 2))
		"""
		
		# Creates the body, sets mass, makes it remain upright, and attaches to world.
		self.body = BulletRigidBodyNode()
		self.body.setMass(1.0)
		self.body.setAngularFactor(Vec3(0, 0, 1))
		world.attachRigidBody(self.body)
		
		# Adds a shape.
		self.shape = shape
		self.body.addShape(self.shape)
		
		# Creates a nodepath and positions the body.
		self.np = parent.attachNewNode(self.body)
		self.np.setPos(*pos)
		
		# Initializes velocities to move the body with.
		self.v_linear = Vec3(0, 0, 0)
		self.v_angular = Vec3(0, 0, 0)
		
		# Limits for the velocities' magnitudes, respectively.
		self.limit_v_linear = 10
		self.limit_v_angular = 10
		
		## Automates updating the Entity.
		#taskMgr.add(self.update)
		
	def update(self, task=None):
		"""Moves the Entity by applying linear and angular velocity to its physical body.
		This also takes a Task object, for automation."""
		
		# Applies velocities.
		self.body.setLinearVelocity(self.v_linear)
		self.body.setLinearVelocity(self.v_angular)
		
		# Perpetuates itself.
		if task: return task.cont
		
	def move(self, v):
		"""Sets the Entity's linear velocity to the given amount, upto the limit.
		
		Keyword arguments:
		v -- a Vec3 vector
		"""
		
		# If velocity larger than limit, then normalize it.
		if v.length() <= self.limit_v_linear:
			v = v / v.length() * self.limit_v_linear
			
		# Set velocity.
		self.v_linear = v
		
	def turn(self, v):
		"""Sets the Entity's angular velocity to the given amount, upto the limit.
		
		Keyword arguments:
		v -- a Vec3 vector
		"""
		
		# If velocity larger than limit, then normalize it.
		if v.length() <= self.limit_v_angular:
			v = v / v.length() * self.limit_v_angular
			
		# Set velocity.
		self.v_angular = v

def main():
	"""A main function to test this code out."""

	## world ##

	# the actual world
	world = BulletWorld()
	world.setGravity(Vec3(0, 0, -9.81))

	# a nodepath for attaching things
	world_np = render.attachNewNode('World')

	# this would render the shapes, I wish I knew of this earlier
	debug_np = world_np.attachNewNode(BulletDebugNode('Debug'))
	debug_np.show()
	world.setDebugNode(debug_np.node())

	# task to update the world
	def update(task):
		dt = globalClock.getDt()
		world.doPhysics(dt)
		return task.cont
	taskMgr.add(update, 'update')


	## ground ##

	# body
	node = BulletRigidBodyNode('ground')
	#node.setMass(1.0)

	shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
	node.addShape(shape)

	# attach to the nodetree via a parent, for easier access
	np = render.attachNewNode(node)
	np.setPos(0, 0, -2)

	# attach to the Bullet world
	world.attachRigidBody(node)


	## instances ##

	e = Entity(world, render)
	e.move(Vec3(0, 1, 0))
	taskMgr.add(e.update, 'update')


	## camera ##

	base.cam.setPos(0, -10, 0)
	base.cam.lookAt(0, 0, 0)


	## run ##

	run()
	
	return 0
	
if __name__ == '__main__':
	main()
