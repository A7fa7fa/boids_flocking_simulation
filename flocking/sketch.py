from random import randrange

from p5.core.primitives import circle
from flocking.flock.flock import Flock
import p5
from flocking.const.constants import WIDTH, HEIGHT



flock = Flock(2)

def setup():
	p5.size(WIDTH, HEIGHT)
	p5.no_stroke()

def draw():
	circ = []

	p5.no_stroke()
	p5.background(0,0,0)
	p5.stroke_weight(1)
	p5.stroke(255)

	for c in circ:
		p5.ellipse(c, 10, 10)
	p5.fill(255)
	fr = str(frame_rate)
	p5.text(fr, WIDTH/2, HEIGHT/2)


	flock.show()
	#print(frame_rate)
	#print(particle.position, particle.velocity, particle.acceleration)

#def key_pressed(event):
#    p5.background(204)

#p5.run(frame_rate = 30)
if __name__ == '__main__':
	p5.run(frame_rate=20)
#p5.run(frame_rate = 30)

def start_local():
	p5.run(frame_rate=30)