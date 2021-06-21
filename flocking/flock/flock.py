from p5.pmath.vector import Vector
from flocking.const.constants import MULT_COHESION, MULT_ALIGNMENT, MULT_SEPARATION
from flocking.flock.particle import Particle
import time

class Flock():

	def __init__(self, size, particles = None) -> None:
		if particles is None:
			self.particles = []
		
			for i in range(size):
				self.particles.append(Particle())
		else:
			self.particles = particles
	
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
		freeze_flock = self.particles[:]

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
				force = particle.flocking(freeze_flock)
				particle.acceleration += force

			if particle.acceleration.magnitude == 0:
				particle.acceleration = particle.prev_acceleration

			particle.update()
		
		frame_time = 1 / 60
		t = int((time.time() - start) * 1000)
		#print(f'Calculation in microsec. {t}')
		if t < frame_time: 
			time.sleep(frame_time-t)
			#print(frame_time - t)




