from random import randrange
from p5.core.attribs import fill, no_fill, stroke_weight, stroke
from p5.core.constants import CENTER
from p5.core.primitives import arc, ellipse, line, triangle
from p5.core.transforms import pop_matrix, push_matrix, rotate, translate
from p5.pmath.utils import HALF_PI, PI, QUARTER_PI, distance
from p5.pmath.vector import Vector

from flocking.const.constants import DRAW_PERCEPTION, MULT_ALIGNMENT, MULT_COHESION, MULT_SEPARATION, WIDTH, HEIGHT, PERCEPTION_RADIUS


class Particle():
	
	id = 0

	def __init__(self) -> None:
		x = randrange(0, WIDTH)
		y = randrange(0, HEIGHT)
		
		self.id = Particle.id

		self.position = Vector(x, y)
		self.velocity = Vector.random_2D() # richtung in der sich das object bewegt
		self.velocity.magnitude = 5 # starting with a greater speed
		self.acceleration  = Vector(0,0)
		self.prev_acceleration = Vector.random_2D()
		self.maxForce = 0.2
		self.maxSpeed = 5

		self.perception = PERCEPTION_RADIUS
		self.free_space = self.perception * 0.3
		self.perception_arc = PI + (QUARTER_PI)

		Particle.id += 1

	def dictify(self):
		dic = {
			'id': self.id, 
			'position': { 
						'x': str(self.position.x), 
						'y': str(self.position.y)
						},
			'velocity': { 
						'x': str(self.velocity.x), 
						'y': str(self.velocity.y)
						},
			'acceleration': { 
						'x': str(self.acceleration.x), 
						'y': str(self.acceleration.y)
						},
			'maxForce': str(self.maxForce),
			'maxSpeed': str(self.maxSpeed),
			'perception': str(self.perception),
			'free_space': str(self.free_space),
			'perception_arc': str(self.perception_arc),
			'start_perception': str(self.start_perception()),
			'end_perception': str(self.end_perception()),
			}
		return dic

	def start_perception(self):
		return self.velocity.angle - (self.perception_arc/2)
	def end_perception(self):
		return self.velocity.angle + (self.perception_arc/2)

	def update(self):
		# newtons law of motion
		# Force = Mass * acceleration
		# or acceleration = Force / mass
		# there is no mass so acceleration = Force
		# euler integration

		self.position += self.velocity # position is updatedt based on the objects velocity
		self.velocity += self.acceleration #velocity is updatedt based on the objects acceleration
		self.velocity.limit(self.maxSpeed) #limit maximum speed of particle
		self.prev_acceleration = self.acceleration
		self.acceleration = Vector(0,0) # reset acceleration. because it is just a calculated force based on the forces in the environment at the given moment in time.
		
		self.edge()


	def edge(self):
		if self.position.x > WIDTH:
			self.position.x = 0
			#self.velocity *= -1
		elif self.position.x < 0:
			self.position.x = WIDTH
			#self.velocity *= -1
		if self.position.y > HEIGHT:
			self.position.y = 0
			#self.velocity *= -1
		elif self.position.y < 0:
			self.position.y = HEIGHT
			#self.velocity *= -1
		

		
	def show(self):
		try:
			stroke_weight(1) #Sets the width of the stroke used for lines, points, and the border around shapes. All widths are set in units of pixels.
			stroke(255) #Set the color used to draw lines around shapes
			#fill(255)
			#ellipse(self.position, 6, 6, mode=CENTER )
			no_fill()
			
			if False:
				tr = Vector(self.velocity.x, self.velocity.y)
				tr.normalize()
				tr.magnitude = 12
				p2 = Vector.from_angle((QUARTER_PI/1.5)+tr.angle)
				p2.magnitude = 12
				p3 = Vector.from_angle((2*PI-(QUARTER_PI/1.5)+tr.angle))
				p3.magnitude = 12
				point1 = self.position + tr
				point2 = self.position - p2
				point3 = self.position - p3
				triangle(point1, point2, point3)
			else:
				with push_matrix():
					translate(self.position.x, self.position.y)
					rotate(self.velocity.angle)
					fill(100)
					point1 = Vector( 10,   0) #oben
					point2 = Vector(-5,  5) #rechts
					point3 = Vector(-5, -5) #links
					triangle(point1, point2, point3)

			
		except Exception as e:
			print(e)

		if DRAW_PERCEPTION:
			# line to display moving direction
			stroke_weight(1)
			stroke(255, 0, 0)
			line(self.position, self.position + (self.velocity*5))

		if DRAW_PERCEPTION:
			# circle to display perception radius
			stroke_weight(1)
			stroke(0, 255, 0)
			no_fill()
			ellipse(self.position, (self.free_space)*2, (self.free_space)*2, mode=CENTER) # x, y, diameter (perception is r so multiplied by 2)
			arc(self.position, self.perception*2, self.perception*2, self.start_perception(), self.end_perception(), mode='PIE')



	def in_perception(self, other, disSq):
		if (self.id == other.id # if other particle is me return false
			or disSq > (self.perception * self.perception)): # if distance to other particle is farther than perception return false 
			return False

		# if other particle is inside of free_space return treu
		elif disSq < (self.free_space * self.free_space): 
			return True

		# if other particle is ouside of perception
		elif disSq > (self.perception * self.perception):
			return False
		
		# if position is inside of perception
		else:			
			v_to_other = other.position - self.position #vector from this position to other position 

			# and position is inside of angle of perception
			# return True
			# else false
			if v_to_other.angle > self.start_perception() and v_to_other.angle < self.end_perception(): return True
			else: return False

	def getSquaredDistance(self, other):
		xDiff = (other.position.x - self.position.x) * (other.position.x - self.position.x)
		yDiff = (other.position.y - self.position.y) * (other.position.y - self.position.y)
		sqDist = xDiff + yDiff 
		return sqDist


	def flocking(self, qTree):
		# align
		avg_velocity = Vector(0, 0)
		# cohesion
		avg_position = Vector(0, 0)
		# separation
		avg_sepa = Vector(0, 0)

		percived_neighbor = 0


		other_points = qTree.queryRactangle(self.position.x, self.position.y, self.perception)
		#print(len(other_points))
		for other in other_points:
			disSq = self.getSquaredDistance(other.userData)
			#dis = self.position.distance(other.userData.position)
			if self.in_perception(other=other.userData, disSq = disSq):
			#if dis < self.perception and particle.id != self.id:
				# align
				avg_velocity += other.userData.velocity
				# cohision
				avg_position += other.userData.position
				# separation
				diff = self.position - other.userData.position # get a vector that is pointing away from local flockmate
				diff /= (disSq * disSq)  # inversly proportional to distance. there farther away it is, the lower is the magnitde
				avg_sepa += diff

				percived_neighbor += 1


		steering_force_align = avg_velocity
		steering_force_cohision = avg_position
		steering_force_sepa = avg_sepa

		if percived_neighbor > 0:
			# align
			steering_force_align /= percived_neighbor
			steering_force_align.magnitude = self.maxSpeed
			steering_force_align -= self.velocity
			steering_force_align.limit(self.maxForce)
			steering_force_align *= MULT_ALIGNMENT
			
			#cohision
			steering_force_cohision /= percived_neighbor
			steering_force_cohision -= self.position
			steering_force_cohision.magnitude = self.maxSpeed
			steering_force_cohision -= self.velocity
			steering_force_cohision.limit(self.maxForce)
			steering_force_cohision *= MULT_COHESION

			#separation
			steering_force_sepa /= percived_neighbor
			steering_force_sepa.magnitude = self.maxSpeed
			steering_force_sepa -= self.velocity
			steering_force_sepa.limit(self.maxForce)
			steering_force_sepa *= MULT_SEPARATION
		steering_force = Vector(0,0)
		steering_force += steering_force_align
		steering_force += steering_force_cohision
		steering_force += steering_force_sepa

		return steering_force



	def align(self, flock): # sets velocity of flock to avg of all flocks in perception radius
		avg_velocity = Vector(0, 0)

		#to find avg of velocity add all up and devide by amount		
		percived_neighbor = 0
		for particle in flock:
			if self.in_perception(other=particle):
			#if self.position.distance(particle.position) < self.perception and particle.id != self.id:
				avg_velocity += particle.velocity
				percived_neighbor += 1

		steering_force = avg_velocity
		if percived_neighbor > 0:
			steering_force /= percived_neighbor

			# Craig Reynolds steering algorithm
			# steering force = steer towards some desired velocity minus current actual velocity
			steering_force.magnitude = self.maxSpeed
			steering_force -= self.velocity
			steering_force.limit(self.maxForce)
			#self.acceleration = self.acceleration + steering_force

			# this is not correct
			#self.velocity = avg_velocity
		return steering_force
		
	def cohesion(self, flock): # sets velocity of flock to avg position of all flocks in perception radius
		avg_position = Vector(0, 0)

		#to find avg of postion add all up and devide by amount		
		percived_neighbor = 0
		for particle in flock:
			if self.in_perception(other=particle):
			#if self.position.distance(particle.position) < self.perception and particle.id != self.id:
				avg_position += particle.position
				percived_neighbor += 1

		steering_force = avg_position
		if percived_neighbor > 0:
			steering_force /= percived_neighbor

			# Craig Reynolds steering algorithm
			# steering force = steer towards some desired postion minus current actual position 
			# results in a vector pointing to the desired postion
			steering_force -= self.position
			
			steering_force.magnitude = self.maxSpeed
			steering_force -= self.velocity

			steering_force.limit(self.maxForce)

		return steering_force
	
	def separation(self, flock): # sets velocity of flock to steer away of position of all flocks in perception radius
		avg_sepa = Vector(0, 0)

		#to find avg of postion add all up and devide by amount		
		percived_neighbor = 0
		for particle in flock:
			d = self.position.distance(particle.position)
			if self.in_perception(other=particle):
			#if d < self.perception and particle.id != self.id:
				diff = self.position - particle.position # get a vector that is pointing away from local flockmate
				diff /= (d * d)  # inversly proportional to distance. there farther away it is, the lower is the magnitde
				avg_sepa += diff
				percived_neighbor += 1

		steering_force = avg_sepa
		if percived_neighbor > 0:
			steering_force /= percived_neighbor

			# Craig Reynolds steering algorithm
			# steering force = steer towards some desired postion minus current actual position 
			# results in a vector pointing to the desired postion
			
			steering_force.magnitude = self.maxSpeed
			steering_force -= self.velocity

			steering_force.limit(self.maxForce)

		return steering_force



