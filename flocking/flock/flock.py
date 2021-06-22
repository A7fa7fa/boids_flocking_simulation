from flocking.flock.quadtree.quadtree import Quadtree
from flocking.const.constants import HEIGHT, MULT_COHESION, MULT_ALIGNMENT, MULT_SEPARATION, WIDTH
from flocking.flock.particle import Particle
from flocking.flock.quadtree.quadtree import Quadtree

import time


class Flock():

	def __init__(self, size, particles = None) -> None:
		self.count = 0

		if particles is None:
			self.particles = []
		
			for i in range(size):
				self.particles.append(Particle())
			self.qTree = self.buildTreeFromParticles()

		else:
			self.particles = particles
	
	def buildTreeFromParticles(self):
		start = time.time()

		qTree = Quadtree(WIDTH, HEIGHT, 4)
		for particle in self.particles:
			qTree.insert(particle.position.x, particle.position.y, userDate = particle)
		
		t = int((time.time() - start) * 1000)
		if self.count % 10 == 0:
			print(f'Tree built in microsec. {t}')
		return qTree

	def dictify(self):
		flock_array = []
		for p in self.particles:
			flock_array.append(p.dictify())
		flock = Flock(size = 0, particles=flock_array)
		return flock.__dict__
	
	def show(self):
		self.calc()
		for particle in self.particles:
			particle.show()
	
	def calc(self):

		start = time.time()
		self.qTree = self.buildTreeFromParticles()
		#freeze_flock = self.particles[:]

		for particle in self.particles:
			if False:
				# force accumilation 
				alignment = particle.align(freeze_flock) * MULT_ALIGNMENT
				particle.acceleration += alignment
				cohesion = particle.cohesion(freeze_flock) * MULT_COHESION
				particle.acceleration += cohesion
				separation = particle.separation(freeze_flock) * MULT_SEPARATION
				particle.acceleration += separation
			else:			
				# not working?
				force = particle.flocking(self.qTree)
				particle.acceleration += force

			if particle.acceleration.magnitude == 0:
				particle.acceleration = particle.prev_acceleration

			particle.update()
		
		frame_time = 30
		t = int((time.time() - start) * 1000)
		self.count += 1
		if self.count % 10 == 0:
			print(f'Flock calculated in microsec. {t} ')
		#if t < frame_time: 
		#	time.sleep(frame_time-t)
		#	print(frame_time - t)




