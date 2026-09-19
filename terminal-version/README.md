# Terminal Version

Cow/wolf/grass game simulation with ASCII output in the terminal.

## Setup

- Install [`uv`](https://docs.astral.sh/uv/) (if not already installed):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Install dependencies:
  ```bash
  uv sync
  ```

## Run

- Start the simulation:
  ```bash
  uv run python main.py
  ```
- Statistics run (CSV export of 10,000 ticks):
  ```bash
  uv run python logging.py
  ```

## Contents

- `main.py` – entry point, starts the simulation in the terminal
- `Board.py` – simulation logic (movement, eating, environment analysis)
- `Creature.py` – classes for Cow, Wolf, Grass
- `hill_climbing.py` – hill climbing example algorithm (independent of the simulation)
- `logging.py` – simulation run with CSV statistics export
