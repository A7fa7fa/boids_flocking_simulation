from flocking.flock.flock import Flock
from networking.server import server

def run():
	# create flock
	flock = Flock(30)
	
	# start sock server and pass flock into it and await connection
	server(flock=flock)


if __name__ == '__main__':
	run()

