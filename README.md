# boids_flocking_simulation
 

Craig Reynolds 1987 Flocking Simulation. https://en.wikipedia.org/wiki/Boids

- Logic of flocking (cohesion, separation, alignment) implemented in python.
- Sending result of every frame to NodeJS-Webserver via TCP Socket streamm.
- NodJS Webserver is hosting static index.html file with p5js script.
- Flocking data is routed from NodeJS to Frontend via Websocket.
