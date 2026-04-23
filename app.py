import streamlit as st

st.set_page_config(page_title="Flappy Bird", layout="centered")

st.title("🐦 Flappy Bird (Press SPACE or Click to Jump)")

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
    outline: none;
}
</style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="500" tabindex="1"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Force focus so keyboard works
canvas.focus();
canvas.addEventListener("click", () => canvas.focus());

let bird, pipes, score, gameOver, gameStarted, countdown, autoFlaps;

// Reset game
function resetGame() {
    bird = { x: 50, y: 250, velocity: 0 };
    pipes = [];
    score = 0;
    gameOver = false;
    gameStarted = false;
    countdown = 3;
    autoFlaps = 2;
    startCountdown();
}

resetGame();

// Create pipes
function createPipe() {
    let height = Math.floor(Math.random() * 200) + 100;
    pipes.push({ x: 400, height: height });
}

// Controls (SPACE + Click)
function flap() {
    if (gameStarted && !gameOver) {
        bird.velocity = -8;
    }
}

document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        flap();
    }
});

canvas.addEventListener("mousedown", flap);

// Countdown
function startCountdown() {
    let interval = setInterval(() => {
        countdown--;
        if (countdown <= 0) {
            clearInterval(interval);
            gameStarted = true;
        }
    }, 1000);
}

// Update
function update() {
    if (gameOver) return;
    if (!gameStarted) return;

    // Auto flaps
    if (autoFlaps > 0) {
        bird.velocity = -6;
        autoFlaps--;
    }

    bird.velocity += 0.5;
    bird.y += bird.velocity;

    if (pipes.length === 0 || pipes[pipes.length - 1].x < 200) {
        createPipe();
    }

    pipes.forEach(pipe => pipe.x -= 3);

    // Collision
    pipes.forEach(pipe => {
        if (pipe.x < 70 && pipe.x > 20) {
            if (bird.y < pipe.height || bird.y > pipe.height + 150) {
                gameOver = true;
            }
        }
    });

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

    // Countdown
    if (!gameStarted) {
        ctx.font = "50px Arial";
        ctx.fillText(countdown > 0 ? countdown : "GO!", 170, 250);
    }

    // Game Over + Restart Button
    if (gameOver) {
        ctx.fillStyle = "red";
        ctx.font = "30px Arial";
        ctx.fillText("Game Over", 120, 220);

        // Restart Button
        ctx.fillStyle = "black";
        ctx.fillRect(140, 250, 120, 40);
        ctx.fillStyle = "white";
        ctx.font = "18px Arial";
        ctx.fillText("Restart", 165, 277);
    }
}

// Restart click detection
canvas.addEventListener("click", function(e) {
    if (gameOver) {
        let rect = canvas.getBoundingClientRect();
        let x = e.clientX - rect.left;
        let y = e.clientY - rect.top;

        if (x >= 140 && x <= 260 && y >= 250 && y <= 290) {
            resetGame();
        }
    }
});

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
