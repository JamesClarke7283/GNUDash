# GNU Dash Plan
GNU Dash is a procedurly generated 2D platformer game, heavily inspired by the Free Software movement and the GNU Foundation.
The goal is to collect `Freedom`, which is a score, as you go and avoid losing `Liberty Shields` which are basically lives, you start off with `5` lives.

Its an infinite side scrolling game, so you have limited time to collect the points, etc. You can pause the game though.

Note: **Please use absolute imports for code when developing the game, so `src.core` instead of `.core`, etc**

## Ideas for mechanics

### **Collectibles (Free/Libre Software Tropes):**
- **Source Code**: Collect source code to increase your Freedom Score by liberating the source code.
- **Freedom Badges**: Pick up badges representing the Four Freedoms of Free Software, if you collect all 4 freedoms, you get a super powerup.
- **Binary Blobs**: Jump on Binary Blobs to increase your score and avoid slowly losing freedom points (if you dont stamp them out then you slowly lose score).

### **Power-Ups:**
- **Freedom Hat**: Wearing a hat (like Richard Stallman’s iconic hat) that temporarily makes you invincible to proprietary software enemies.
- **Source Shield**: A shield made of source code that protects you from enemies and obstacles for a limited time.
- **GPL Scroll**: A scroll that, when collected, releases the power of the GPL, destroying all proprietary software enemies on the screen.
- **Libre Boost**: A power-up that gives you a speed boost, allowing you to move faster and jump higher, symbolizing the freedom of fast and efficient software.
- **Forked Power**: A power-up that allows you to create a "fork" of yourself, temporarily duplicating your character to tackle multiple challenges simultaneously.
- **Free Software Potion**: A potion that temporarily increases your abilities, like double jumping or stronger attacks, representing the empowerment that comes with free software.

### **Enemies (Proprietary Software Tropes):**
- **DRM Drones**: Flying enemies that represent Digital Rights Management (DRM), trying to restrict your movement or abilities.
- **Closed Source Cubes**: Blocky enemies that symbolize closed-source software, trying to trap you or block your path.
- **Spyware Spiders**: Creepy-crawly enemies that represent surveillance software, trying to follow and capture you.
- **Patent Trolls**: Enemies that represent patent trolls, attempting to slow you down or steal your progress.
- **Corporate Chains**: Chains or barriers that represent proprietary corporations, trying to restrict your access to certain areas or features

## Code files

Here is some code files we already have that you can interact with.

### Logging
Please include logging throughout the code at different log levels and use the `get_logger` function, this is the sourcecode file we have already placed.
`src/logging.py`:
```python
import os
import sys
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from appdirs import user_log_dir
import coloredlogs

def setup_logging(app_name: str = "GNUDash") -> logging.Logger:
    load_dotenv()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = user_log_dir(app_name)
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, f"{app_name.lower()}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(app_name)
    coloredlogs.install(level=LOG_LEVEL, logger=logger)

    # Add TRACE log level
    TRACE = 5
    logging.addLevelName(TRACE, "TRACE")
    setattr(logger, "trace", lambda message, *args: logger.log(TRACE, message, *args))

    return logger

# Global logger instance
logger: Optional[logging.Logger] = None

def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = setup_logging()
    return logger
```
### Pyproject Toml Config file
`./pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=45", "setuptools_scm[toml]>=6.2", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "GNUDash"
dynamic = ["version"]
description = "A GNU (Gnu's Not Unix) inspired Platformer game, Collect Source code points, avoid DRM, and have fun."
authors = [
    {name = "James David Clarke", email = "james@jamesdavidclarke.com"},
]
license = {text = "GPL-3.0-or-later"}
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
]

dependencies = [
    "pillow",
    "pygame",
    "python-dotenv",
    "coloredlogs",
    "appdirs"
]

[project.optional-dependencies]
dev = [
    "black",
    "isort",
    "mypy",
]

[project.urls]
Homepage = "https://github.com/JamesClarke7283/GNUDash"
"Bug Tracker" = "https://github.com/JamesClarke7283/GNUDash/issues"

[tool.setuptools]
packages = ["src"]

[project.scripts]
gnudash = "src.main:main"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

## Project Structure
```
.
├── assets - Contains all webp image files for assets.
│   └── LICENSE
├── docs
│   ├── LICENSE.md
│   └── PLAN.md
├── LICENSE.md
├── pyproject.toml
├── README.md
└── src
    ├── components - Contains all the Pygame related code as components, there will be a pygame component version of the player and a code version of the player which will be in core for example.
    ├── core - All logic code goes in here, we must seperate the Graphics rendering from the game logic by putting game logic in core.
    ├── main.py - Contains the `main` method which runs the pygame loop, it starts with a `Main Menu`
    ├── main_menu.py - Contains the main menu scene.
    ├── game.py - Contains the Game scene which is the actual platformer.
    └── logging.py
```

## Seperation of Code and Data:
To keep data seperate from code, we have a `.default_config.toml` file in the root of the project, this must contain all constants, please use the builtin `tomllib` library for reading this, we can have a `src/config.py` to give us the config data.

## Type Hints and Docstrings
Please include type hints in all code, and use Docstrings where possible.

## Plan for development

### Phase 1: Creating basic Menu & Game

Make a main menu with the `Play` button to start the game, make it easy so if we want to add more buttons we can.
When we click play it starts the game.

We can only move UP,DOWN (its scrolling right all the time so we get sideways movement, we only need up and down controls). You can use the UP/DOWN arrow keys or the W & S keys to move.

Create A basic counter for "Freedom: 0" and "Liberty Shields: 5" for now. the default number of lives will be stored in the `.default_config.toml`.

In `src/core` we need a `player.py` to define the player class, there will also be a `player.py` in `components` which is the pygame rendering of the player.

We collect "Source Code" to gain more points.

At this phase i just want to have the Source Code increase the points by 1 each time, we wont put anything that removes shields yet.
Most focus is on generating the level procedurely, the levels dont get "harder" they just get "different" so sometimes it will be harder than other times.

We won't have any asset files yet, but in a later phase we can add them.

You can pause the game at any point with the escape key to bring up the pause menu. where you can either `Continue` or `Exit`.

We need to generate a set of `Block`'s so we have places to jump up to and not fall down.