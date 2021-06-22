const ws = new WebSocket("ws://localhost:8080/ws"); // connects to this adress

var flock;

var show_perc = false

//milisekunden 
var start = new Date().getTime();
var count = 0;

function setup() {
	createCanvas(1280, 1280/2);
	strokeWeight(5);
	frameRate(40)


	 // event emmited when connected
	 ws.onopen = function () {
		console.log('websocket is connected ...')
		// sending a send event to websocket server
		ws.send('connected')
	}
	// event emmited when receiving message 
	ws.onmessage = function (ev) {
		//buff = Buffer.from(ev.data, 'utf8');
		d = ev.data.toString();
		try {
			flock = JSON.parse(d)
			//flock = dj['particles']
		}
		catch (e){
			console.log(e)
		}
		count++;
		if (new Date().getTime() - start > 10000) {
			console.log(`Send frames ${count/10}; Print frames ${frameRate()}`);
			count = 0;
			start = new Date().getTime();
		}
	}
	  
}

function draw(){
	background(51);
	
	stroke(255);
	fill(100);
	strokeWeight(1);
	ellipse(mouseX, mouseY, 60, 60);
	if (flock) {
		f = flock['particles'];
		//console.log(f[0].acceleration)
		for (var i = 0; i < f.length; i++) {             
			show(particle=f[i]);
		}
	}

}

function show(particle){
	push();

	stroke(255);
	strokeWeight(2)
	fill(100);

	velocity = createVector(parseFloat(particle.velocity.x), parseFloat(particle.velocity.y));
	position = createVector(parseFloat(particle.position.x), parseFloat(particle.position.y));
	translate(position);
	rotate(velocity.heading());
	triangle(10,0,-5,5,-5,-5);
	
	pop(); 
	
	strokeWeight(1)
	// velocity
	stroke(255, 0, 0);
	line(position.x, position.y, position.x + (velocity.x*5), position.y + (velocity.y*5));

	if (show_perc){
		// circle to display perception radius
		stroke(0, 255, 0);
		noFill();
		ellipse(particle.position.x, particle.position.y, (particle.free_space)*2, (particle.free_space)*2);
		arc(particle.position.x, particle.position.y, 
			particle.perception*2, particle.perception*2, 
			particle.start_perception, particle.end_perception, 
			mode=PIE);
		}

	 
}
