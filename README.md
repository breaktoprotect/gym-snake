# Description
My very own Snake game implemented in OpenAI Gym. There are many out there, but there's none like this. :D
I'm a control freak so I like to have control over the environment itself, thus created this for education and flexibility.

# Details
## How does the game works?
Standard Snake game. If you owned a Nokia phone ever, you would have played this game. 

## Source
TODO

## Observations
4 x Collision detection (next step)
4 x Apple "GPS" - Above, right-of, below, left-of (global)
1 x Scalar distance between Apple and Snake's head
1 x If snake ate an apple this round

## Actions
0 - Up
1 - Right
2 - Down
3 - Left

Pressing the movement while in the same direction yields no action. 
For example, if the snake is facing North, press Up will effectively do nothing.

## Reward System
Reward is given when an action is performed, be it positive, neutral or negative (points).

### Simple reward
- Every time the snake eats the red apple (1 point)

### Slightly more complex reward
- Every time the snake doesn't bump into things (1 points)
- Every time the snake move closer to the red apple on either the x or y axes (2 points)
- Every time the snake eats the red apple (100 points)

### More complex reward
- To include: Every 100 steps without eating red apple (-100 points)

### Current Experiment Reward
- Every time snake moves closer to red apple (0.01 point)
- Every time snake eats apple (10 points)
- Every time snake dies (-1 point)

## Starting State:
Snake starts at a random position within a given boundary
Apple appears at a random position throughout accessible positions in the environment. Changes position whenever it gets eaten.

## Episode Termination:
Snake collides with wall or itself.