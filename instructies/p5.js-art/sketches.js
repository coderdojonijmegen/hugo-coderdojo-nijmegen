// having multiple sketches on a single page: http://joemckaystudio.com/multisketches/

let frameRate = 15;
new p5(function(ctx) {
    var circle = 200;
    var rot;
    var col;
    var freq = 0.000005;
    var cont = 0;
    var r;

    ctx.setup = function() {
        ctx.createCanvas(600, 600);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function() {
        ctx.background(255);
        ctx.translate(300, 300);
        ctx.rotate(ctx.radians(rot));

        ctx.ellipseMode(ctx.RADIUS);
        for (var i=0; i<500; i ++) {
            circle= 200 + 50 * ctx.sin(ctx.millis() * freq * i);
            col = ctx.map(circle, 150, 250, 255, 60);
            r= ctx.map(circle, 150, 250, 5, 2);
            ctx.fill(col, 0,74);
            ctx.noStroke();
            ctx.ellipse(circle * ctx.cos(i), circle * ctx.sin(i), r, r);
            rot= rot + 0.00005;
        }
    }
}, 'demo');


new p5(function(ctx) {
    ctx.setup = function() {
        ctx.createCanvas(150, 150);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function() {
        ctx.background(255);
        ctx.translate(ctx.width / 2, ctx.height / 2);
        ctx.rotate(ctx.frameCount / 50);
        ctx.rect(-26, -26, 52, 52);
    }
}, 'voorbeeld1')


new p5(function(ctx) {
    ctx.setup = function() {
        ctx.createCanvas(710, 400);
        ctx.background(102);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function() {
        let speed = ctx.abs(ctx.mouseX - ctx.pmouseX) + ctx.abs(ctx.mouseY - ctx.pmouseY);
        ctx.stroke(speed);
        ctx.fill(ctx.color(150 - speed, speed, 128 + speed))
        ctx.ellipse(ctx.mouseX, ctx.mouseY, speed, speed);
    }
}, 'voorbeeld2')
