import p5
from p5.core.constants import CENTER
from p5.core.font import text
from p5.core.primitives import rect

import time

from flocking.const.constants import WIDTH, HEIGHT


class Point():
	def __init__(self, x_, y_, userData_ = None) -> None:
		self.x = x_
		self.y = y_
		self.userData = userData_


class Quadtree():

	def __init__(self, width_, height_, capacity_) -> None:
		self.level = 0
		self.x = width_ / 2
		self.y = height_ / 2
		self.width = width_
		self.height = height_

		self.capcity = capacity_

		self.segment = Quadtree.Segment(self.x, self.y, self.width / 2, self.height / 2, self.level)

		
	def insert(self, x, y, userDate = None):
		start = time.time()

		# adds point to tree
		point = Point(x, y, userDate)
		self.segment.insert(point)

		t = int((time.time() - start) * 1000)
		#print(f'Insert point in microsec. {t}')

	
	def queryRactangle(self, x, y, range) -> list:
		start = time.time()

		result = self.segment.query(Point(x, y), range, mode = 'Rectangle')

		t = int((time.time() - start) * 1000)
		#print(f'Calculation points {len(result)} in microsec. {t}')
		
		return result

	def queryCircle(self, x, y, range) -> list:
		start = time.time()

		result = self.segment.query(Point(x, y), range, mode = 'Circle')

		t = int((time.time() - start) * 1000)
		print(f'Calculation in microsec. {t}')
		
		return self.returnPoints(result)


	def show(self):
		# p5 depenecy
		# draws points and segments
		self.segment.show()


	class Segment():

		def __init__(self, x_, y_, width_, height_, level_) -> None:
			self.x = x_
			self.y = y_
			self.width = width_
			self.height = height_
			self.level = level_ + 1

			self.southWest:Quadtree.Segment = None
			self.southEast:Quadtree.Segment = None
			self.northWest:Quadtree.Segment = None
			self.northEast:Quadtree.Segment = None

			self.capacity = 4
			self.points = []

			self.children = False

			# draw intersected segment in a diff collour
			self.intersects = False


		def insert(self, point:Point):
			if self.isInside(point):
				# point is in this segmtn

				if self.children == False:
					# segment hast no childs
					
					if self.hasCapacity():
						# segment has capacity
						# so add point to this segment
						return self.addPoint(point)
					else:
						# segment has no capacity
						# so create child segments
						# and pass point to childsegments
						self.createChilds()
						return self.insertIntoChildren(point)

				elif self.children == True:
					# segment has childsegments
					# pass point to child segment
					return self.insertIntoChildren(point)
				else: 
					print('ERROR: this should not have happend')
					return False
			else:
				# point is not in this segment
				return False



		def addPoint(self, point:Point) -> bool:
			# add point to segment
			self.points.append(point)
			return True
			

		def insertIntoChildren(self, point:Point) -> bool:
			# insert point into childsegment
			# returns True if point is inside of bounds of child
			# else False and next child is checked
			if self.southWest.insert(point):
				return True
			elif self.southEast.insert(point):
				return True
			elif self.northWest.insert(point):
				return True
			elif self.northEast.insert(point):
				return True
			else:
				print('point is in no child', self.children, self.level, self.x, self.y,  point.x, point.y)
				return False


		def hasCapacity(self) -> bool:
			# returns true if segment has capacity to add points to
			return len(self.points) < self.capacity


		def isInside(self, point) -> bool:
			# returns true if point is inside of boundary of this segment
			# favours East Segment if x position of point is on x boundary
			# favours south Segment if y position of point is on y boundary
			return (point.x >= (self.x - (self.width)) 
				and point.x < (self.x + (self.width)) 
				and point.y >= (self.y - (self.height)) 
				and point.y < (self.y + (self.height)))


		def createChilds(self):
			# creates childsegments for this segemnt
			# childsegments are width / 2 and heigth / 2
			w = self.width / 2
			h = self.height / 2
			self.southWest = Quadtree.Segment(x_ = self.x - w, y_ = self.y - h, width_ = w, height_ = h, level_ = self.level)
			self.southEast = Quadtree.Segment(x_ = self.x + w, y_ = self.y - h, width_ = w, height_ = h, level_ = self.level)
			self.northWest = Quadtree.Segment(x_ = self.x - w, y_ = self.y + h, width_ = w, height_ = h, level_ = self.level)
			self.northEast = Quadtree.Segment(x_ = self.x + w, y_ = self.y + h, width_ = w, height_ = h, level_ = self.level)
			self.children = True
			#print('children created')

		def query(self, p_, range, mode = 'Rectangle') -> list:
			# returns list of intersected points
			points = []
			if mode == 'Rectangle':
				
				# if this range not intersects - return None
				if not self.intersectsRectangle(p_, range): 
					#print('not intersect')
					return points
				else:
					if self.children == True:
						# if children exists call recursice query of childsegment and add result list to this result list 
						points += self.southWest.query(p_, range, mode = mode)
						points += self.southEast.query(p_, range, mode = mode)
						points += self.northWest.query(p_, range, mode = mode)
						points += self.northEast.query(p_, range, mode = mode)

					# append points of this segment which are inside of rectangle to resultlist					
					points += self.pointsOfSegmentInsideRectangle(p_, range)

					# return result to quadtree or parentsegment
					return points

			elif mode == 'Circle':
				# TODO
				return points

		def intersectsRectangle(self, p_, range):
			# return true if center is inside of segment
			self.intersects = False
			if self.isInside(p_): 
				#print('center is inside')
				self.intersects = True
				return True

			# return false if rectangle is outside of segment
			elif ((self.x + self.width <= p_.x - range) 
				or (self.x  - self.width >= p_.x + range)
				or (self.y + self.height <= p_.y - range)
				or self.y - self.height >= p_.y + range):
				self.intersects = False
				return False
			
			# else rectangle overlapps
			else: 
				#print('overlaps')
				self.intersects = True
				return True
		
		def pointsOfSegmentInsideRectangle(self, p_, range):
			# returns points which are inside of rectangle

			points = []
			for p in self.points:	
				if  (p.x >= (p_.x - (range)) 
					and p.x <= (p_.x + (range)) 
					and p.y >= (p_.y - (range)) 
					and p.y <= (p_.y + (range))):
					points.append(p)

			return points

		def show(self):
			# p5 depenecy
			# draws points and segments
			p5.stroke(0, 255, 100)
			p5.stroke_weight(1)

			# draws intersected segments in a different collour
			if self.intersects:
				p5.stroke_weight(5)
				p5.stroke(255,0,0)
				self.intersects = False
				
			p5.no_fill()
			#p5.rect(self.x, self.y, self.width * 2 - 10, self.height * 2 - 10, mode = CENTER)

			for p in self.points:
				p5.stroke_weight(5)
				p5.stroke(255)
				p5.fill(100)
				p5.ellipse(p.x, p.y, 10, 10)

			if self.children:
				self.southWest.show() 
				self.southEast.show() 
				self.northWest.show()
				self.northEast.show()

	
				

def setup():
	p5.size(WIDTH, HEIGHT)
	qtree = Quadtree(WIDTH, HEIGHT, 4)
	for i in range(1000):
		x = p5.random_uniform(WIDTH, WIDTH)
		y = p5.random_uniform(HEIGHT, HEIGHT)
		qtree.insert(x, y)
	
	p5.translate(WIDTH / 2, HEIGHT / 2)
	p5.background(0,0,0)
	p5.no_fill()
	p5.stroke_weight(2)
	p5.stroke(255)
	qtree.show()

