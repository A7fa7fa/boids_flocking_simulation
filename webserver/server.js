

const express = require('express');
const http = require('http')
const WebSocketServer = require('ws').Server
const utf8 = require('utf8')
const uit = new TextEncoder('utf-8')

var app = express();
app.use(express.static('public'));

var BACKEND_ADDR = '192.168.0.171'
var BACKEND_PORT = 5051

var WEBSERVER_PORT = 8080

//init simple http server
var server = http.createServer(app);

//init websocket server instance
var wss = new WebSocketServer({server: server, path: "/ws"});

server.listen(WEBSERVER_PORT); //webserver is listening on this port
console.log(`My Socket Server is listening on ${WEBSERVER_PORT}.`);


const net = require('net');
const client = new net.Socket();
connect();
//client.setEncoding('utf-8');


//client.connect(BACKEND_PORT, BACKEND_ADDR, function(){
//	console.log(`Connected to flockingServer on ${BACKEND_ADDR}:${BACKEND_PORT}`)
//	client.write(encode_string('Node Server started!'))
//});



wss.on('connection', function (ws, req) {
	ws.on('message', function (message) {
	  console.log('received: %s', message)
	})	
	//client.write(encode_string(`${new Date()}`))
	console.log(`${ws._socket.remoteAddress}`);
	client.write(encode_string(`${req.socket.remoteAddress}`));

	var data_string = ""
	client.on('data', function(data){

		//d = decode_string(data.toString())
		var buff = Buffer.from(data, 'utf-8');
		data_string = data_string + buff.toString();
		var msg_leght = ""
		var msg = ""
		var base_length = data_string.length
		//console.log(data_string.length);

		while (data_string.length > 0 ) {
			// get msg length
			msg_leght = data_string.slice(0,6).split("{")[0].toString();

			// get msg from buffer by msg_length
			msg = data_string.slice(msg_leght.length, msg_leght.length + parseInt(msg_leght) );

			// delete msg from buffer
			data_string = data_string.slice(msg_leght.length + parseInt(msg_leght));
			
			try {
				flock = JSON.parse(msg)
				ws.send(msg)
				//console.log(flock)
				//flock = dj['particles']
			}
			catch (e){
				console.log("Fail")
				data_string = ""
				break
			}
			//console.log(data_string.length);
			//console.log(data_string);
			//console.log(msg);
		}
	});


	ws.on('close', function(){
		console.log('connection closed!')
	});
	
  });


client.on('error', function(err){
	if (err.code === 'ECONNRESET'){
		console.log("backend not available")
		try {
			connect(); 
		} catch (error) {
			console.log(error)
		}

	}  else {
		console.log(err)
	}
});

function connect(){
	client.connect(BACKEND_PORT, BACKEND_ADDR);
	//client.setTimeout(10000);
	
	client.on('timeout', () => {
		client.destroy();
		connect(); 
	});		
	client.setEncoding('utf-8');
	console.log(`Connected to flockingServer on ${BACKEND_ADDR}:${BACKEND_PORT}`)

}



client.on('close', function(){
	console.log('connection closed!')
	//connect(); 
});


function encode_string(str){
	
	str_len = uit.encode(str).length;
	while (str_len.toString().length < 4){
		str_len = '0' + str_len;
	};	
	s = uit.encode(str_len+str);
	return (s);
};


function intFromBytes(array) {
    var value = 0;
    for (var i = 0; i < array.length; i++) {
        value = (value * 256) + array[i];
    }
    return value;
}

function decode_string(bstr){
	str = uit.encode(bstr)
	return str.slice(4)
};
