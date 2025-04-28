
# Ticket to Ride - Python Implementation

A Python implementation of the famous board game **Ticket to Ride** (*Les Aventuriers du Rail*), originally designed by **Alan R. Moon** and published by **Days of Wonder**.

This project provides a playable version of the game, focusing on implementing its core mechanics clearly and efficiently.

---

## Features

- Implementation of main game mechanics:
  - Capturing routes
  - Drawing wagon cards (with locomotive handling)
  - Completing destination tickets
- Unit testing using Python's `unittest` module
- Clear class architecture for readability and maintenance

## Requirements

- Python 3.7+
- networkx for class diagram generation and map / Plateau graphic generation
- matplotlib used in diverse plotting functions

- (use of unittest, random and unittest.mock for testing)

might need to enter the following line to prevent uninstalled package malfunctioning

  pip install -r requirements.txt

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
├── LesAventuriersDuRail.py       # Core classes and game logic
├── Lancement.py                  # Entry point to launch the game
├── Tests.py                      # Unit tests (run with unittest)
├── Diag_classe.py                # Generates class diagrams
├── diagramme_classes_aventuriers_du_rail.gv # Class diagram file
├── myplot.png                    # Generated class diagram image
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation (this file)
```

## Running tests

To run all unit tests, execute:

```bash
python Tests.py
```
use of unittest

## Future improvements

- Basic AI player (random choices ignoring new destination cards)
- Graphical User Interface (supposedly using PyQt5)

## Disclaimer

This project is made for **educational purposes only** and is not intended for commercial use. All rights to the original game belong to Alan R. Moon and Days of Wonder.

---

© Lancelot RAMIS - 2025
