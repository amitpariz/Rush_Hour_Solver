Rush Hour - AI Final Project
----------------------------
  
Running the program
-------------------

"Games.py" is the main file, so to run the program, the following command needs to be executed (via the shell): "python Games.py",
or alternatively, run Game.py in python IDE such as pycharm. Some input will be required:
•	First, the difficulty of the game needs to be selected, by pressing 1 for easy, 2 for medium, 3 for hard.
•	Then, the search algorithm needs to be selected, by pressing 1 for A* and 2 for IDA*
•	Last, the heuristic needs to be selected, there are 9 difference heuristics and 
	they are listed on screen for the user to choose from.
After the three parameters were selected, the AI solver prints the boards and the steps it chose on
its way to the goal state (the solution).


Files
-------
README - This file.
Vehicle.py - represents a vehicle object.
Board.py - represents a game Board object.
RushHourSearch.py - here are implementations and definitions of the problem, the search algorithms, and heuristics.
Util.py - several utilities used in the program.
Game.py - the main file that runs the program.
level files - found in the 'cards' folder, these are 40 possible levels of the Rush Hour game.
