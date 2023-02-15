

console.log('loaded');

let boids = [];
let canvasWidth = window.innerWidth;
let canvasHeight = window.innerHeight;
let boidcount = 200;
let processing = false;
let scrollDelta = 0;
let c;

console.log(canvasWidth)
console.log(canvasHeight)

function setup() {
	c = createCanvas(canvasWidth, canvasHeight);
	c.position(0,0);
	c.background(0,0);
	c.id('flockingCanvas');
	
	
	//document.getElementById("flockingCanvas").style.display = 'none';
	
	// Add an initial set of boids into the system
	
	let paragraphs = document.getElementsByTagName("p");
	console.log(paragraphs[0]);

	var wordDict = {};

	let count = 0;
	for (let i = 0; i < paragraphs.length; i++) {
		words = paragraphs[i].innerHTML.split(" ");
		for (let j = 0; j < words.length; j++) {
			if (window.find(words[j], false, false, true, false, false, false)) {
				var rect = window.getSelection().getRangeAt(0).getBoundingClientRect();
				boids.push(new Boid(random(width), random(height), rect.right, rect.y))
				count++
			}
		}
		if (count >= boidcount) {
			break;
		}
	}
	
	if (count < boidcount) {
		for (let i = 0; i<boidcount - count;i++) {
			boids.push(new Boid(random(width), random(height), -1, -1));
		}
	}
}

function mouseWheel(event) {

  scrollDelta += event.delta;
  print(scrollDelta);

	c.position(0,scrollDelta);
	//uncomment to block page scrolling
	  //return false;

}

function draw() {
  clear()
  // Run all the boids
  for (let i = 0; i < boids.length; i++) {
	boids[i].run(boids);
  }
  
  
}

var s2 = function( sketch ) {
	sketch.setup = function() {
		let canvas2 = sketch.createCanvas(canvasWidth, canvasHeight);
		canvas2.position(0,0);
		canvas2.background(255,55);
		canvas2.id('hiddenCanvas');
		
		//window.addEventListener('resize', resizeAllCanvas);
		
	}
	
	sketch.draw = function() {
		if (mouseIsPressed === true) {
			sketch.line(sketch.mouseX, sketch.mouseY, sketch.pmouseX, sketch.pmouseY);
			sketch.stroke(25);
			startedDrawing = true;
		}
	}
	
	sketch.mouseReleased = function() {
		sketch.clear();
		sendPattern();
	}
};

// create the second instance of p5 and pass in the function for sketch 2
new p5(s2);

function sendPattern() {
	if (!processing) {
		patternCanvas = document.getElementById("hiddenCanvas");
		let dataURL = patternCanvas.toDataURL();
		dataURL = dataURL.replace(/^data:image\/[a-z]+;base64,/, "");
		console.log(dataURL)

		let hook_url = "http://127.0.0.1:5002/hook"

		let data = new FormData();
		data.append("data",dataURL);

		// send data to the server and fetch back response
		
		processing = true;
		fetch(hook_url, {
		method: "POST",
		body: data
		}).then(response => response.text)
		.then(text => data.value = text);
		processing = false;
	}
}

function resizeAllCanvas(){
	
	const hiddenCanvas = document.getElementById("hiddenCanvas");
	const hiddenCTX = hiddenCanvas.getContext('2d');
	
	const flockingCanvas = document.getElementById('flockingCanvas');
	const flockingCTX = flockingCanvas.getContext('2d');

    flockingCTX.canvas.width = window.innerWidth;
    flockingCTX.canvas.height = window.innerHeight;
	
	hiddenCTX.canvas.width = window.innerWidth;
    hiddenCTX.canvas.height = window.innerHeight;
    }
