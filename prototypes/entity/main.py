from pandac.PandaModules import *
import direct.directbase.DirectStart
from panda3d.bullet import *

class Entity(DirectObject):
	
	def __init__(self, world, parent, shape=BulletCapsuleShape(0.5, 1), pos=(0, 0, 2)):
		"""Creates a generic Entity with a physical component.

		Keyword arguments:
		world -- a panda3d.bullet.BulletWorld object to add the Entity's physical body to
		parent -- the Node under which the Entity's physical body will be added
		shape -- a panda3d.bullet.BulletShape object for the Entity's physical body (default BulletCapsuleShape(0.5, 1))
		pos -- a three-tuple for the position of the Entity with respect of its parent (default (0, 0, 2))
		"""
		
		# Creates the body.
		self.body = BulletRigidBodyNode()
		self.body.setMass(1.0)
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
		self.limit_v_linear = 1
		self.limit_v_angular = 1
		
		## Automates updating the Entity.
		#taskMgr.add(self.update)
		
	def update(self):
		"""Moves the Entity by applying linear and angular velocity to its physical body."""
		
		# Applies velocities.
		self.body.setLinearVelocity(self.v_linear)
		self.body.setLinearVelocity(self.v_angular)


