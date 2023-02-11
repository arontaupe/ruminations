console.log('loaded');

let boids = [];
let canvasWidth = window.innerWidth;
let canvasHeight = window.innerHeight;
let boidcount = 200;
console.log(canvasWidth)
console.log(canvasHeight)

if (true) {
	function setup() {
		let c = createCanvas(canvasWidth, canvasHeight);
		c.position(0,0);
		
		background(0,0);
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

	function draw() {
	  clear()
	  // Run all the boids
	  for (let i = 0; i < boids.length; i++) {
		boids[i].run(boids);
	  }
	}
}