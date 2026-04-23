import streamlit as st

st.set_page_config(page_title="Flappy Bird", layout="centered")

st.title("🐦 Flappy Bird (Easy Mode + High Score)")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
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

// Ensure focus for keyboard
canvas.focus();
canvas.addEventListener("click", () => canvas.focus());

// SETTINGS (EASY MODE)
const gravity = 0.3;
const jumpPower = -7;
let pipeSpeed = 2;
const pipeGap = 180;

// Safe best score load
let bestScore = parseInt(localStorage.getItem("flappyBest")) || 0;

// Game variables
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
    pipeSpeed = 2;
    startCountdown();
}

resetGame();

// Create pipe
function createPipe() {
    let height = Math.floor(Math.random() * 180) + 120;
    pipes.push({ x: 400, height: height, passed: false });
}

// Controls
function flap() {
    if (gameStarted && !gameOver) {
        bird.velocity = jumpPower;
    }
}

// Keyboard
document.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        e.preventDefault();
        flap();
    }
});

// Mouse
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

// Update game
function update() {
    if (gameOver || !gameStarted) return;

    // Auto start boost
    if (autoFlaps > 0) {
        bird.velocity = -5;
        autoFlaps--;
    }

    bird.velocity += gravity;
    bird.y += bird.velocity;

    // Pipes
    if (pipes.length === 0 || pipes[pipes.length - 1].x < 220) {
        createPipe();
    }

    pipes.forEach(pipe => pipe.x -= pipeSpeed);

    // Collision
    pipes.forEach(pipe => {
        if (pipe.x < 75 && pipe.x > 15) {
            if (bird.y < pipe.height - 5 || bird.y > pipe.height + pipeGap + 5) {
                gameOver = true;
            }
        }
    });

    // Ground
    if (bird.y > 500 || bird.y < 0) {
        gameOver = true;
    }

    // Score
    pipes.forEach(pipe => {
        if (!pipe.passed && pipe.x < 50) {
            pipe.passed = true;
            score++;

            if (score > bestScore) {
                bestScore = score;
                localStorage.setItem("flappyBest", bestScore);
            }

            if (score % 5 === 0) {
                pipeSpeed += 0.2;
            }
        }
    });
}

// Draw
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Bird
    ctx.beginPath();
    ctx.arc(bird.x, bird.y, 12, 0, Math.PI * 2);
    ctx.fillStyle = "yellow";
    ctx.fill();

    // Pipes
    pipes.forEach(pipe => {
        ctx.fillStyle = "green";
        ctx.fillRect(pipe.x, 0, 40, pipe.height);
        ctx.fillRect(pipe.x, pipe.height + pipeGap, 40, 500);
    });

    // Score
    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText("Score: " + score, 10, 25);
    ctx.fillText("Best: " + bestScore, 280, 25);

    // Countdown
    if (!gameStarted) {
        ctx.font = "50px Arial";
        ctx.fillText(countdown > 0 ? countdown : "GO!", 160, 250);
    }

    // Game Over
    if (gameOver) {
        ctx.fillStyle = "red";
        ctx.font = "30px Arial";
        ctx.fillText("Game Over", 120, 220);

        ctx.fillStyle = "black";
        ctx.fillRect(140, 250, 120, 40);
        ctx.fillStyle = "white";
        ctx.font = "18px Arial";
        ctx.fillText("Restart", 165, 277);
    }
}

// Restart button
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

// Game loop
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
