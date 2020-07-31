import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import random
import numpy as np

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.ENV_HEIGHT = 500 
        self.ENV_WIDTH = 500
        self.VELOCITY = 10 # How much to move per unit  
        self.action_space = spaces.Discrete(4)
        self.SEGMENT_WIDTH = 10

        # Render using pygame
        self.window = pygame.display.set_mode((self.ENV_HEIGHT, self.ENV_WIDTH))

        #* State
        # Snake starting position
        #TODO randomize starting
        self.snake_segments = [(250,250),(250,260),(250,270),(250,280),(250,290)]
        self.facing = 0 # 0 is up, 1 is right, 2 is down, 3 is left #TODO random.randrange(0,4)

        # Apple starting position
        self.apple_pos = self._spawn_apple()

        # 'Done' state
        self.done = False

    def step(self, action):
        # Ignore action if step and direction is the same
        if action != self.facing:
            # Update the new snake direction
            self.facing = action
 
        # Advance the snake
        self._move_snake()
        self.done = self._check_collision()
        reward = self._check_eaten()

        #TODO observations

        return None, reward, self.done, {}

    def reset(self):
        # Snake starting position
        #TODO randomize starting
        self.snake_segments = [(250,250),(250,260),(250,270),(250,280),(250,290)]
        self.facing = 0 # 0 is up, 1 is right, 2 is down, 3 is left #TODO randomize
        # Apple starting position
        self.apple_pos = self._spawn_apple()

        # 'Done' state
        self.done = False
  
        return #? need to return state?

    def render(self, mode='human', close=False):
        #* Draw & Display
        self.window.fill((0,0,0)) # Clear screen to color black again
        # Snake
        for segment in self.snake_segments:
            pygame.draw.rect(self.window, (25,205,75), (segment[0], segment[1], self.SEGMENT_WIDTH, self.SEGMENT_WIDTH))
        # Apple
        pygame.draw.rect(self.window, (205,25,25), (self.apple_pos[0], self.apple_pos[1], self.SEGMENT_WIDTH, self.SEGMENT_WIDTH))
        pygame.display.update()
            
        return

    def _move_snake(self):
        snake_head = (0,0)
        if self.facing == 0:
            snake_head = np.subtract(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        if self.facing == 1:
            snake_head = np.add(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))
        if self.facing == 2:
            snake_head = np.add(self.snake_segments[0], (0, self.SEGMENT_WIDTH))
        if self.facing == 3:
            snake_head = np.subtract(self.snake_segments[0], (self.SEGMENT_WIDTH, 0))

        leftovers = self.snake_segments[:-1]
        self.snake_segments = [] #reset
        self.snake_segments.append(tuple(snake_head))
        for segment in leftovers:
            self.snake_segments.append(segment)

        #debug 
        print("_move_snake()::self.snake_segments (new snake):", self.snake_segments)

    def _check_collision(self):
        # Borders
        if self.snake_segments[0][0] == self.ENV_HEIGHT or self.snake_segments[0][1] == self.ENV_WIDTH + self.SEGMENT_WIDTH or \
            self.snake_segments[0][0] == -self.SEGMENT_WIDTH or self.snake_segments[0][1] == -self.SEGMENT_WIDTH:
            print("[!] Snake crashed to the wall! Exiting...")
            return True

        # Snake itself
        if np.any(tuple(self.snake_segments[0]) in self.snake_segments[1:]):
            print("[!] Snake crashed itself! Exiting...")
            return True

        return False

    def _check_eaten(self):
        if self.snake_segments[0] == self.apple_pos:
            print("[+] NOM!")
        else:
            return False

        #* Growing the snake
        additional_segment = self.snake_segments[len(snake_segments)-1:]

        if facing == 0: 
            additional_segment = np.add(additional_segment, (0, SEGMENT_WIDTH))
        if facing == 1:
            additional_segment = np.subtract(additional_segment, (SEGMENT_WIDTH, 0))
        if facing == 2:
            additional_segment = np.subtract(additional_segment, (0, SEGMENT_WIDTH))
        if facing == 3:
            additional_segment = np.add(additional_segment, (SEGMENT_WIDTH, 0))

        self.snake_segments.append(tuple(additional_segment[0]))

        #* Respawn Apple at random location
        self.apple_pos = self._spawn_apple()

        return True

    def _spawn_apple(self):
        return (random.randrange(0,50) * self.SEGMENT_WIDTH, random.randrange(0,50) * self.SEGMENT_WIDTH)