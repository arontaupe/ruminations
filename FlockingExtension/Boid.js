// Boid class
// Methods for Separation, Cohesion, Alignment added
class Boid {
  constructor(x, y, wordx, wordy) {	
    this.acceleration = createVector(0, 0);
    this.velocity = p5.Vector.random2D();
    this.position = createVector(x, y);
    this.r = 3.0;
    this.maxspeed = 6;    // Maximum speed
    this.maxforce = 0.1; // Maximum steering force
	
	this.text = '';
	this.textMaxLength = 20;
	this.textTime = Date.now();
	this.maxTextTime = 5 * 1000;
	this.minTextTime = 2 * 1000;
	this.color = this.randomColor();
	
	this.age = 0;
	this.halfLife = 300 + int(Math.random() * 700);
	
	this.wordx = wordx;
	this.wordy = wordy;
  }
  
  die() {
	  this.position = createVector(random(width), random(height));
	  this.age = 0;
	  this.color = this.randomColor();
  }
  
  multiply(boids) {
	boids.push(new Boid(this.position.x + random(10) - 10, this.position.y + random(10) - 10));
  }
  
  perish(boids) {
	boids = boids.slice(0, this.index).concat(boids.slice(this.index + 1));
	console.log(boids.length);
	delete this;
	console.log(false);
  }

  run(boids) {  
	if (this.age > this.halfLife * 2) {
		this.die()
	}
	this.flock(boids);
	this.update();
	this.borders();
	this.render(boids);
  }
  
  
  // Forces go into acceleration
  applyForce(force) {
    this.acceleration.add(force);
  }
  
  // We accumulate a new acceleration each time based on three rules
  flock(boids) {
    let sep = this.separate(boids); // Separation
    let ali = this.align(boids);    // Alignment
    let coh = this.cohesion(boids); // Cohesion
	let lis = this.listeriosis(boids); // Direction
    // Arbitrarily weight these forces
    ali.mult(0.2);
    coh.mult(0.1);
	
	if (mouseIsPressed === true) {
		lis.mult(10.0);
		sep.mult(10.0);
	} else {
		lis.mult(0.3);
		sep.mult(0.6);
	}
	
	
    // Add the force vectors to acceleration
    this.applyForce(sep);
    this.applyForce(ali);
    this.applyForce(coh);
	this.applyForce(lis);
  }
  
  // Method to update location
  update() {
    // Update velocity
    this.velocity.add(this.acceleration);
    // Limit speed
    this.velocity.limit(this.maxspeed);
    this.position.add(this.velocity);
    // Reset acceleration to 0 each cycle
    this.acceleration.mult(0);
  }
  
  // A method that calculates and applies a steering force towards a target
  // STEER = DESIRED MINUS VELOCITY
  seek(target) {
    let desired = p5.Vector.sub(target, this.position); // A vector pointing from the location to the target
    // Normalize desired and scale to maximum speed
    desired.normalize();
    desired.mult(this.maxspeed);
    // Steering = Desired minus Velocity
    let steer = p5.Vector.sub(desired, this.velocity);
    steer.limit(this.maxforce); // Limit to maximum steering force
    return steer;
  }
  
  
  randomText() {
	return (Math.random() + 1).toString(36).substring(int(Math.random() * this.textMaxLength));
  }
  
  randomColor() {
	  const colors = ["orange", "grey", "darkgrey", "black", "white"];
	  return color(colors[int(Math.random() * colors.length)])
  }
    
  // Draw boid as a random text
  render(boids) {
	textSize(10);
	var now = Date.now();
	this.age++;
	
	if (this.text == '' || ((now - this.textTime) > this.minTextTime + int(Math.random() * this.maxTextTime))) {
		this.text = this.randomText()
		text(this.randomText(20), this.position.x, this.position.y);
		
		this.textTime = now;
	}
	
	var colorValue;
	if (this.age <= this.halfLife) {
		colorValue = (int((this.age / this.halfLife) * 255))
	} else {
		colorValue = 255 - int(((this.age - this.halfLife) / this.halfLife) * 255)
	}
	this.color.setAlpha(colorValue);
		
	//render text
	text(this.text, this.position.x, this.position.y);
	fill(this.color);
	
	//render connections
	let desiredseparation = 25.0;
	for (let i = 0; i < boids.length; i++) {
      let d = p5.Vector.dist(this.position, boids[i].position);
      if ((d > 0) && (d < desiredseparation)) {
        line(this.position.x, this.position.y, boids[i].position.x, boids[i].position.y)
		stroke(this.color);
      }
    }
	
	//render wordlines
	
	if (this.wordx >= 0) {
		if (p5.Vector.dist(this.position, createVector(this.wordx, this.wordy)) >= 800) {
			line(this.position.x, this.position.y, this.wordx, this.wordy);
			stroke(this.color);
		}
	}
  }
  
  // Wraparound
  borders() {
    if (this.position.x < -this.r) this.position.x = width + this.r;
    if (this.position.y < -this.r) this.position.y = height + this.r;
    if (this.position.x > width + this.r) this.position.x = -this.r;
    if (this.position.y > height + this.r) this.position.y = -this.r;
  }
  
  // Direct
  listeriosis(boids) {
	  
	let listeriosisTarget = createVector(mouseX, mouseY);
	let steer = p5.Vector.sub(listeriosisTarget, this.position);
	try {
		steer.normalize();
		steer.limit(this.maxforce);
		return steer;
	} catch (error) {
		return createVector(0,0);
	}
	
  }
  
  // Separation
  // Method checks for nearby boids and steers away
  separate(boids) {
    let desiredseparation = 25.0;
    let steer = createVector(0, 0);
    let count = 0;
    // For every boid in the system, check if it's too close
    for (let i = 0; i < boids.length; i++) {
      let d = p5.Vector.dist(this.position, boids[i].position);
      // If the distance is greater than 0 and less than an arbitrary amount (0 when you are yourself)
      if ((d > 0) && (d < desiredseparation)) {
        // Calculate vector pointing away from neighbor
        let diff = p5.Vector.sub(this.position, boids[i].position);
        diff.normalize();
        diff.div(d); // Weight by distance
        steer.add(diff);
        count++; // Keep track of how many
      }
    }
    // Average -- divide by how many
    if (count > 0) {
      steer.div(count);
    }
  
    // As long as the vector is greater than 0
    if (steer.mag() > 0) {
      // Implement Reynolds: Steering = Desired - Velocity
      steer.normalize();
      steer.mult(this.maxspeed);
      steer.sub(this.velocity);
      steer.limit(this.maxforce);
    }
    return steer;
  }
  
  // Alignment
  // For every nearby boid in the system, calculate the average velocity
  align(boids) {
    let neighbordist = 50;
    let sum = createVector(0, 0);
    let count = 0;
    for (let i = 0; i < boids.length; i++) {
      let d = p5.Vector.dist(this.position, boids[i].position);
      if ((d > 0) && (d < neighbordist)) {
        sum.add(boids[i].velocity);
        count++;
      }
    }
    if (count > 0) {
      sum.div(count);
      sum.normalize();
      sum.mult(this.maxspeed);
      let steer = p5.Vector.sub(sum, this.velocity);
      steer.limit(this.maxforce);
      return steer;
    } else {
      return createVector(0, 0);
    }
  }
  
  // Cohesion
  // For the average location (i.e. center) of all nearby boids, calculate steering vector towards that location
  cohesion(boids) {
    let neighbordist = 50;
    let sum = createVector(0, 0); // Start with empty vector to accumulate all locations
    let count = 0;
    for (let i = 0; i < boids.length; i++) {
      let d = p5.Vector.dist(this.position, boids[i].position);
      if ((d > 0) && (d < neighbordist)) {
        sum.add(boids[i].position); // Add location
        count++;
      }
    }
    if (count > 0) {
      sum.div(count);
      return this.seek(sum); // Steer towards the location
    } else {
      return createVector(0, 0);
    }
  }  
}