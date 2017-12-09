 # Blue Barracuda's Clue-less Project
This game is a simplified version of the popular board game, Clue. The main simplification is in the navigation of the game board. In Clue-Less there are the same nine rooms, six weapons, and six people as in the board game. The rules are pretty much the same except for moving from room to room. 

### Table of Contents
**[Prerequisites](#prerequisites)**<br>
**[Usage](#usage)**<br>
**[Game Rules](#game-rules)**<br>
**[Tests](#tests)**<br>
**[Development](#development)**<br>
**[Authors](#authors)**<br>

## Prerequisites
There are only two dependencies required to run the game, and an additional dependency to run the tests:
* [Python3](https://www.python.org/downloads/release/python-363/)
* [Pygame](https://www.pygame.org/)
* [Pytest](https://docs.pytest.org/)

## Usage
One player must be running the "server" that allows each of the players to connect as clients. After the server is running all players then will simply use Python3 to launch the gameapp.py file.

## Game Rules
1. The rooms are laid out in a 3x3 grid with a hallway separating each pair of adjacent rooms. (See game board image below)
2. Each hallway only holds one person. If someone is currently in a hallway, you may not move there.
3. When it is your turn, you don’t need to roll a die. Your options of moving are limited to the following:
   - If you are in a room, you may do one of the following:
       - Move through one of the doors to the hallway (if it is not blocked).
       - Take a secret passage to a diagonally opposite room (if there is one) and make a suggestion.
       - If you were moved to the room by another player making a suggestion, you may, if you wish, stay in that room and make a suggestion. Otherwise you may move through a doorway or take a secret passage as described above.
   - If you are in a hallway, you must do the following:
       - Move to one of the two rooms accessible from that hallway and make a suggestion.
       - If all of the exits are blocked (i.e., there are people in all of the hallways) and you are not in one of the corner rooms (with a secret passage), and you weren’t moved to the room by another player making a suggestion, you lose your turn (except for maybe making an accusation).
4. Your first move must be to the hallway that is adjacent to your home square. The inactive characters stay in their home squares until they are moved to a room by someone making a suggestion.
5. Whenever a suggestion is made, the room must be the room the one making the suggestion is currently in. The suspect in the suggestion is moved to the room in the suggestion.
6. You may make an accusation at any time during your turn.
7. Here are the [original rules](https://www.hasbro.com/common/instruct/clueins.pdf) for the game.
### Game Board
![alt text](https://github.com/yo09975/Clue-less/blob/master/resources/gameplaygui.jpg "Game GUI")

## Tests
Comprehensive unit and integration testing modules have been included. Tests can be run individually, or by utilizing Pytest on the Clue-less/tests/ directory.

## Development
Extensive source control processes were implemented for this project. In order to contribute, development must be directly related to an Issue which has been confirmed by two or more developers as required work.

Once an issue is confirmed it can be moved from the Backlog to be In Progress. At that point, a git branch must be created specific to the work being done on that issue.

Once development has been completed in a branch, a peer review is required. Peer reviews have been extremely beneficial to the project, directly leading to quality assurance work and the satisfaction of the project's requirements. Once development has been peer reviewed and all issues have been reconciled, it is moved to the Reviewed stage. The git branch for the development is then merged into the integ branch and staged to be merged into the master branch.

## Authors
* @yo09975
* @brentongk
* @patmay
* @michael-s-myer
* @stephensmeal
