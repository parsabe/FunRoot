# Chess PyGame

<img src="https://github.com/parsabe/FunRoot/blob/master/Chess%20py%20game/logo.gif">
This is a Python-based chess game where you can play against the computer using the Stockfish chess engine. The game uses `pygame` for the graphical interface and `python-chess` for the game logic.

## Features

- Play as either white or black.
- Interactive graphical interface.
- Highlights the selected piece with a red border.
- Stockfish engine for computer moves.

## Requirements

- Python 3.6 or higher
- `pygame` library
- `python-chess` library
- Stockfish engine

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/chess-game.git
    cd chess-game
    ```

2. **Install the required libraries:**
Make sure you have already created a Virtual Environment for Pip to install.
    ```sh
    pip install pygame chess
    ```

3. **Download and setup the Stockfish engine:**

    - Download the Stockfish engine from the official website: [Stockfish Downloads](https://stockfishchess.org/download/)
      or you can simply download from the repository's release packages. <a href="https://github.com/parsabe/FunRoot/releases/tag/stockfish-chess">click here</a> 
    - Extract the downloaded file and place the `stockfish.exe` in a known location.
    - Update the `STOCKFISH_PATH` variable in the script with the path to your `stockfish.exe`.

4. **Prepare the image files:**

    - Ensure the following image files are placed in an `images` directory within the project directory:
        - `wP.png`
        - `bP.png`
        - `wN.png`
        - `bN.png`
        - `wB.png`
        - `bB.png`
        - `wR.png`
        - `bR.png`
        - `wQ.png`
        - `bQ.png`
        - `wK.png`
        - `bK.png`

## Usage

1. **Run the script:**

    ```sh
    python chess_game.py
    ```

2. **Choose your color:**
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Pygame](https://www.pygame.org/)
- [Python-Chess](https://python-chess.readthedocs.io/en/latest/)
- [Stockfish](https://stockfishchess.org/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

    - Input 'W' for white or 'B' for black when prompted.

3. **Play the game:**
    - Click on a piece to select it and click on the destination square to move it.
    - The selected piece will be highlighted with a red border.
    - The computer will make its move after you.



