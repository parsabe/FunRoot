<!DOCTYPE html>
<html>
<head>
    <title>2048 Game - Python Version</title>
</head>
<body>
    <h1>2048 Game (Python Edition)</h1>

    <h2>Overview</h2>
    <p>
        2048 is a single-player sliding tile puzzle game. The objective is to slide numbered tiles on a grid 
        to combine them and create a tile with the number 2048.
    </p>

    <h2>Features</h2>
    <ul>
        <li>4×4 board with smooth animations (GUI version)</li>
        <li>Playable via arrow keys (Up, Down, Left, Right)</li>
        <li>Score tracking</li>
        <li>Game over and win detection</li>
        <li>Replay support</li>
        <li>Written in Python using Tkinter</li>
    </ul>

    <h2>How to Play</h2>
    <ol>
        <li>Use the arrow keys (← ↑ ↓ →) to move all tiles in the chosen direction.</li>
        <li>When two tiles with the same number collide, they merge into one with the sum of both tiles.</li>
        <li>After each move, a new tile (2 or 4) appears in an empty spot on the board.</li>
        <li>Your goal is to reach the 2048 tile.</li>
        <li>The game ends when there are no valid moves left.</li>
    </ol>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>tkinter (included with most Python distributions)</li>
    </ul>

    <h2>Installation & Run</h2>
    <pre>
# Clone or copy the script
python3 2048.py
    </pre>

    <h2>Controls</h2>
    <ul>
        <li><b>Arrow Keys:</b> Move tiles</li>
        <li><b>Close Window:</b> Exit the game</li>
    </ul>

    <h2>About the Code</h2>
    <p>
        The game logic follows the original 2048 algorithm:
        moving, compressing, and merging rows/columns, spawning new tiles, and tracking score.
    </p>
    <p>
        Animations are handled using the built-in <code>tkinter.Canvas</code> with the <code>after()</code> method to simulate motion.
    </p>

    <h2>License</h2>
    <p>
        This project is open-source and available for personal and educational use.
    </p>

    <h2>Author</h2>
    <p>
        Created by [Your Name] — inspired by the original 2048 by Gabriele Cirulli.
    </p>
</body>
</html>

