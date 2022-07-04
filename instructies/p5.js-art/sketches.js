// having multiple sketches on a single page: http://joemckaystudio.com/multisketches/

let frameRate = 15;
new p5(function (ctx) {
    var circle = 200;
    var rot;
    var col;
    var freq = 0.000005;
    var cont = 0;
    var r;

    ctx.setup = function () {
        ctx.createCanvas(600, 600);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function () {
        ctx.background(255);
        ctx.translate(300, 300);
        ctx.rotate(ctx.radians(rot));

        ctx.ellipseMode(ctx.RADIUS);
        for (var i = 0; i < 500; i++) {
            circle = 200 + 50 * ctx.sin(ctx.millis() * freq * i);
            col = ctx.map(circle, 150, 250, 255, 60);
            r = ctx.map(circle, 150, 250, 5, 2);
            ctx.fill(col, 0, 74);
            ctx.noStroke();
            ctx.ellipse(circle * ctx.cos(i), circle * ctx.sin(i), r, r);
            rot = rot + 0.00005;
        }
    }
}, 'demo');


new p5(function (ctx) {
    ctx.setup = function () {
        ctx.createCanvas(150, 150);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function () {
        ctx.background(255);
        ctx.translate(ctx.width / 2, ctx.height / 2);
        ctx.rotate(ctx.frameCount / 50);
        ctx.rect(-26, -26, 52, 52);
    }
}, 'voorbeeld1')


new p5(function (ctx) {
    ctx.setup = function () {
        ctx.createCanvas(710, 400);
        ctx.background(102);
        ctx.frameRate(frameRate);
    }

    ctx.draw = function () {
        let speed = ctx.abs(ctx.mouseX - ctx.pmouseX) + ctx.abs(ctx.mouseY - ctx.pmouseY);
        ctx.stroke(speed);
        ctx.fill(ctx.color(255 - speed, speed, 128 + speed))
        ctx.ellipse(ctx.mouseX, ctx.mouseY, speed, speed);
    }
}, 'voorbeeld2')

/*
    Enkele functies zoals noLoop(), loop(), keyCode lijken niet te werken.
    Hierom gebruikt de demo (voor nu) enkel mouseClicked input...
*/
new p5(function (ctx) {
    let doelwitten;
    let levens;
    let spelerIsDood;
    let krimpSnelheid;

    function init() {
        doelwitten = [];
        levens = 5;
        spelerIsDood = false;
        krimpSnelheid = 0.1;

        ctx.createCanvas(400, 400);
        ctx.frameRate(frameRate);

        //voeg begin doelwitten toe
        doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
        doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
        doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
        doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
        doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
    }

    ctx.mouseClicked = function () {
        if (spelerIsDood) {
            init();
            return;
        }

        for (var i = doelwitten.length - 1; i >= 0; i--) {
            t = doelwitten[i];

            //Bereken de afstand tussen de muis en het doelwit
            let afstand = ctx.dist(ctx.mouseX, ctx.mouseY, t.x, t.y);

            if (afstand < t.d / 2) { //Als de afstand kleiner is dan de halve diameter (radius) van het doelwit is het raak
                doelwitten.splice(i, 1); //Verwijder het doelwit dat geraakt is
                doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
                return;
            }
        }
    }

    ctx.setup = function () {
        init();
    }

    ctx.draw = function () {
        ctx.background(255);
        ctx.text("Levens: " + ctx.str(levens), 20, 20, 100, 100);


        if (spelerIsDood) {
            ctx.textSize(52);
            ctx.text("Klik hier om het spel op te starten. ", 50, 50, 300, 400);
            ctx.textSize(32);
            return;
        }

        for (var i = doelwitten.length - 1; i >= 0; i--) {
            t = doelwitten[i];

            //Teken alle doelwitten
            ctx.ellipse(t.x, t.y, t.d, t.d);

            //Krimp alle doelwitten
            t.d -= krimpSnelheid;

            //verwijder te kleine doelwitten
            if (t.d < 0) { //Is de grootte kleiner dan 0? Dan verwijderen
                doelwitten.splice(i, 1); //Haal het doelwit uit de lijst.
                doelwitten.push({ x: ctx.random(300), y: ctx.random(300), d: 50 }) //Voeg een doelwit toe op een nieuwe willekeurige plek.
                levens--;
            }
        }

        if (levens <= 0) {
            spelerIsDood = true;
        }
    }

}, 'game0')