# Breakout-Game

This project is a homework assignment from CSCI 121 taught by Mark Hopkins.

- `breakout.py`: Most of my code is in this file.
- `config.py`: Contains information about how to configure a particular game of Breakout.
- `graphics.py`: Contains code for displaying the graphics.

There are three versions  of the game that can be run from a Terminal:
- `simple.py`: A simple version of Breakout, useful for testing code.
- `classic.py`: The classic arcade version of Breakout.
- `bunsen.py`: This is the version of Breakout with Dr. Bunsen Honeydew as the target.

## Standard instructions
Click once to start the game. Move your mouse to move the platform. Make sure the platform catches the ball so that it can bounce back and eliminate bricks. You win the game when all bricks are eliminated! 

Make sure the file that contains your desired version of game includes `from breakout import BreakoutGame` at the beginning to play with the standard rules.

## Extensions

The code for the extensions are in `breakout_modified.py`. Make sure to change to `from breakout_modified import BreakoutGame` to play with this new set of rules! 

The goal of the game is the gain as many points as possible. 

Score system:
- Each brick is worth 20 points. 
- If the ball hits several bricks before returning to the paddle, each consecutive brick is worth 10 more points, for example:
  - the second brick in a row is worth 30 points, so two consecutive bricks worth 50 points, 
  - the third brick in a row is worth 40 points, so three consecutive bricks worth 90 points, etc.
- Raw score: The total amount of points gained by hitting bricks is calculated only if all bricks are cleared. 
- Additional points: At the end of the game, each unused ball is worth 100 additional points.
- Final score: (Raw score + Additional points ) * (100% + bonus)

**Different modes of playing**:
There are three modes: easy mode, hard mode, and challenge mode. 
The easy mode only requires the player to hit every brick, whereas the hard mode encourages players to hit consecutive bricks. 
The hard mode has a 50% bonus when calculating the final score, and the easy mode has no bonus. 
Hence by choosing the hard mode, the player may earn more points, but also risks loosing more points. 

Easy mode:
The goal is the total number of bricks times 20. 
So the player will definitely reach the goal if all bricks are cleared. 
There will be no increase to the final score. 

Hard mode:
The goal is higher than easy mode by approximately half the total amount of bricks times 20. 
So the player must hit bricks consecutively to reach the goal.
If the player's raw score does not meet the goal, the player‘s score will be deducted ten times the difference between the score and the goal (you may even get a negative score!). 
There will be a 50% increase to the final score. 

Challege mode: 
Challenge mode has the same basic rules (goal etc.) as the easy mode. 
However, there are two additional springs at the bottom that the ball may hit. 
The ball may speed up or slow down depending on the specific spring. 
There is also a timer in the challenge mode. Although it is not factored into the final score, the player is welcome to challenge himself/herself to achieve a shorter time. 
Thus, the player may purposefully decide to not catch the ball and let it fall onto the speeding up spring. 

