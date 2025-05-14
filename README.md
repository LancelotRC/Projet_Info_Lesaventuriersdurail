
# Ticket to Ride - Python Implementation

A Python implementation of the famous board game **Ticket to Ride** (*Les Aventuriers du Rail*), originally designed by **Alan R. Moon** and published by **Days of Wonder**.

This project was developed as part of an academic software project at ENSTA Bretagne. It aims to simulate the core mechanics of the board game, focusing on object-oriented modeling, modular design, and graph algorithms.

---

## Features

- Core gameplay mechanics implemented:
  - Drawing wagon cards (visible and hidden, with locomotive constraints)
  - Capturing routes (with card validation and wagon cost)
  - Assigning and storing destination tickets
  - Turn-by-turn gameplay management with player prompts
  - Real-time graphical display of the game board (using `matplotlib`)
  - Endgame detection (final turn when a player has ≤2 wagons)
  - Partial scoring system (route points handled)
- Unit tests with `unittest` (and `unittest.mock` for input simulation)

## Requirements

- Python 3.7+
- `networkx` for graph handling and route connectivity
- `matplotlib` for board visualization
- `unittest` and `unittest.mock` for testing
- `random`, `collections`, and standard Python libraries

To install dependencies:

```bash
pip install -r requirements.txt
```

## Quickstart

Clone this repository and launch the game:

```bash
git clone https://github.com/YOUR_USERNAME/AventuriersDuRail.git
cd AventuriersDuRail
python Lancement.py
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Project Structure

```plaintext
AventuriersDuRail/
├── LesAventuriersDuRail.py       # Main classes and game logic
├── Lancement.py                  # Entry point for manual game execution
├── Tests.py                      # Unit tests with unittest
├── Diag_classe.py                # Class diagram generator
├── diagramme_classes_*.gv       # Auto-generated diagram files
├── myplot.png                    # Generated diagram image
├── figures/                      # Image outputs (for reports or GUI)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Running tests

To run all unit tests, execute:

```bash
python Tests.py
```
use of unittest

## Future improvements

- **AI player (random)**: execute legal moves randomly for automatic gameplay
- **Scoring enhancements**:
  - Checking completed objectives using graph connectivity
  - Detecting the longest continuous route (DFS)
- **Graphical User Interface (GUI)**: planned evolution using PyQt5 or Tkinter
- **Human player assistance**:
  - Visual reminders of completed/pending objectives
  - Warnings when objectives are close to being unachievable

## Disclaimer

This project is made for **educational purposes only** and is not intended for commercial use. 
All rights to the original game belong to Alan R. Moon and Days of Wonder.

---

© Lancelot RAMIS - 2025
