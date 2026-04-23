import streamlit as st
import time
import random
import json
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Flappy Bird 🐦", layout="centered")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #70c5ce, #ffffff);
}
.game-box {
    border-radius: 20px;
    padding: 10px;
    text-align: center;
}
.score {
    font-size: 28px;
    font-weight: bold;
    color: #333;
}
.btn {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ CLASSES ------------------
class Bird:
    def __init__(self):
        self.y = 250
        self.velocity = 0

    def flap(self):
        self.velocity = -8

    def update(self):
        self.velocity += 0.5  # gravity
        self.y += self.velocity


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 300)
        self.gap = 150
        self.passed = False

    def update(self, speed):
        self.x -= speed


class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = [Pipe(400)]
        self.score = 0
        self.speed = 3
        self.running = True

    def update(self):
        self.bird.update()

        # Add new pipes
        if self.pipes[-1].x < 200:
            self.pipes.append(Pipe(400))

        # Update pipes
        for pipe in self.pipes:
            pipe.update(self.speed)

            # Score update
            if not pipe.passed and pipe.x < 50:
                pipe.passed = True
                self.score += 1
                self.speed += 0.2  # difficulty increase

        # Remove off-screen pipes
        self.pipes = [p for p in self.pipes if p.x > -50]

        # Collision detection
        for pipe in self.pipes:
            if (pipe.x < 70 and pipe.x > 20):
                if (self.bird.y < pipe.height or 
                    self.bird.y > pipe.height + pipe.gap):
                    self.running = False

        # Ground collision
        if self.bird.y > 500 or self.bird.y < 0:
            self.running = False


# ------------------ LEADERBOARD ------------------
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(score):
    data = load_leaderboard()
    data.append(score)
    data = sorted(data, reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)


# ------------------ SESSION STATE ------------------
if "game" not in st.session_state:
    st.session_state.game = None
if "state" not in st.session_state:
    st.session_state.state = "start"
if "paused" not in st.session_state:
    st.session_state.paused = False


# ------------------ START SCREEN ------------------
if st.session_state.state == "start":
    st.title("🐦 Flappy Bird")
    st.markdown("### Click Start to Play")

    if st.button("▶ Start Game"):
        st.session_state.game = Game()
        st.session_state.state = "play"
        st.rerun()


# ------------------ GAME LOOP ------------------
elif st.session_state.state == "play":
    game = st.session_state.game

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("⬆ Flap"):
            game.bird.flap()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸ Pause"):
            st.session_state.paused = not st.session_state.paused
    with col2:
        if st.button("🔄 Restart"):
            st.session_state.game = Game()
            st.rerun()

    game_area = st.empty()

    while game.running:
        if not st.session_state.paused:
            game.update()

        # Draw game
        html = f"""
        <div class="game-box">
            <div class="score">Score: {game.score}</div>
            <svg width="400" height="500" style="background:#87CEEB;border-radius:10px">
                <!-- Bird -->
                <circle cx="50" cy="{game.bird.y}" r="10" fill="yellow" />

                <!-- Pipes -->
        """

        for pipe in game.pipes:
            html += f"""
                <rect x="{pipe.x}" y="0" width="40" height="{pipe.height}" fill="green"/>
                <rect x="{pipe.x}" y="{pipe.height + pipe.gap}" width="40" height="500" fill="green"/>
            """

        html += "</svg></div>"

        game_area.markdown(html, unsafe_allow_html=True)

        time.sleep(0.03)

    # Game Over
    save_score(game.score)
    st.session_state.state = "game_over"
    st.rerun()


# ------------------ GAME OVER ------------------
elif st.session_state.state == "game_over":
    st.title("💀 Game Over")

    score = st.session_state.game.score
    st.markdown(f"## Your Score: {score}")

    leaderboard = load_leaderboard()

    st.markdown("### 🏆 Leaderboard")
    for i, s in enumerate(leaderboard):
        st.write(f"{i+1}. {s}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again"):
            st.session_state.game = Game()
            st.session_state.state = "play"
            st.rerun()
    with col2:
        if st.button("🏠 Home"):
            st.session_state.state = "start"
            st.rerun()