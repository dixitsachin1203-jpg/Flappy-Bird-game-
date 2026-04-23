import streamlit as st

st.set_page_config(page_title="Flappy Bird Spacebar", layout="centered")

st.title("🐦 Flappy Bird (Press SPACE to Jump)")

# Embed HTML + JS game inside Streamlit
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    overflow: hidden;
    background: linear-gradient(to bottom, #70c5ce, #ffffff);
}
canvas {
    display: block;
    margin: auto;
    background: #87CEEB;
    border-radius: 10px;
}
</style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="500"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let bird = { x: 50, y: 200, velocity: 0 };
let gravity = 0.5;
let pipes = [];
let score = 0;
let gameOver = false;

// Generate pipes
function createPipe() {
    let height = Math.floor(Math.random() * 200) + 100;
    pipes.push({ x: 400, height: height });
}

// Spacebar control
document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        bird.velocity = -8;
    }
});

// Game loop
function update() {
    if (gameOver) return;

    bird.velocity += gravity;
    bird.y += bird.velocity;

    // Create pipes
    if (pipes.length === 0 || pipes[pipes.length - 1].x < 200) {
        createPipe();
    }

    // Move pipes
    pipes.forEach(pipe => pipe.x -= 3);

    // Collision
    pipes.forEach(pipe => {
        if (pipe.x < 70 && pipe.x > 20) {
            if (bird.y < pipe.height || bird.y > pipe.height + 150) {
                gameOver = true;
            }
        }
    });

    // Ground collision
    if (bird.y > 500 || bird.y < 0) {
        gameOver = true;
    }

    // Score
    pipes.forEach(pipe => {
        if (!pipe.passed && pipe.x < 50) {
            pipe.passed = true;
            score++;
        }
    });
}

// Draw
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Bird
    ctx.beginPath();
    ctx.arc(bird.x, bird.y, 10, 0, Math.PI * 2);
    ctx.fillStyle = "yellow";
    ctx.fill();

    // Pipes
    pipes.forEach(pipe => {
        ctx.fillStyle = "green";
        ctx.fillRect(pipe.x, 0, 40, pipe.height);
        ctx.fillRect(pipe.x, pipe.height + 150, 40, 500);
    });

    // Score
    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 10, 25);

    if (gameOver) {
        ctx.fillStyle = "red";
        ctx.font = "30px Arial";
        ctx.fillText("Game Over", 120, 250);
    }
}

// Loop
function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

st.components.v1.html(game_html, height=520)
